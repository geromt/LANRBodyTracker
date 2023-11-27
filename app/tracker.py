import math

import cv2
import socket
import mediapipe as mp

from app.config_reader import ConfigReader, CoordinatesType


class HandTracker:
    def __init__(self, config: ConfigReader):
        self.capture = cv2.VideoCapture(config.camera_index)
        self.port = config.port
        self.frame_height = config.frame_height
        self.frame_width = config.frame_width

        self.display_video = config.display_video
        self.display_video_size = config.display_video_size
        self.draw_hand = config.draw_hand
        self.mpDraw = mp.solutions.drawing_utils

        if config.config_frame:
            self.capture.set(3, self.frame_width)
            self.capture.set(4, self.frame_height)

        self.mpHands = mp.solutions.hands
        self.detector = self.mpHands.Hands(static_image_mode=config.static_mode,
                                           max_num_hands=config.max_hands,
                                           model_complexity=config.model_complexity,
                                           min_detection_confidence=config.min_detection_confidence,
                                           min_tracking_confidence=config.min_tracking_confidence)

        self.server_address_port = ("127.0.0.1", self.port)

        self.include_type = config.type
        self.include_height = config.include_height
        self.include_width = config.include_width
        self.coordinates = config.coordinates
        self.lm_list = self._calc_landmark_list(config.lm_list)
        self.include_box = config.include_box
        self.include_center = config.include_center
        self.print_data = config.print_data

    def _process_capture(self):
        success, img = self.capture.read()

        if not success:
            return

        data, img = self.find_hands(img)
        if not data:
            data.append("NoHand")

        return img, data

    def capture_and_send(self):
        """
        Captura los movimientos de la mano y manda los datos por el puerto especificado. Para conocer la estructura de
        los datos revisar README.md
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while True:
                img, data = self._process_capture()
                if data:
                    s.sendto(str.encode(str(data)), self.server_address_port)
                    if self.print_data:
                        print(str.encode(str(data)))

                if self.display_video:
                    img = cv2.resize(img, (
                        self.frame_width // self.display_video_size,
                        self.frame_height // self.display_video_size))
                    cv2.imshow("Image", img)
                    cv2.waitKey(1)

    def find_hands(self, img, flipType=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :return: Image with or without drawings
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.detector.process(img_rgb)
        hand_data = []
        h, w, c = img.shape

        if self.coordinates == CoordinatesType.REAL_WORLD:
            multi_hand_landmarks = results.multi_hand_world_landmarks
        else:
            multi_hand_landmarks = results.multi_hand_landmarks

        if multi_hand_landmarks:
            for handType, handLms in zip(results.multi_handedness, multi_hand_landmarks):
                if self.include_type:
                    if flipType:
                        if handType.classification[0].label == "Right":
                            hand_data.append("Left")
                        else:
                            hand_data.append("Right")
                    else:
                        hand_data.append(handType.classification[0].label)

                if self.include_height:
                    hand_data.append(h)
                if self.include_width:
                    hand_data.append(w)

                lm_list = []
                landmarks = handLms.landmark

                for lm in self.lm_list:
                    lm_coor = landmarks[lm]
                    if self.coordinates == CoordinatesType.PIXEL:
                        px, py, pz = int(lm_coor.x * w), int(lm_coor.y * h), int(lm_coor.z * w)
                    else:
                        px, py, pz = lm_coor.x, lm_coor.y, lm_coor.z
                    lm_list.append([px, py, pz])

                if self.include_box or self.include_center:
                    x_vals = (lm.x if self.coordinates == CoordinatesType.PIXEL else (lm.x * w) for lm in landmarks)
                    x_min, x_max = self._find_min_max(x_vals)

                    y_vals = (lm.y if self.coordinates == CoordinatesType.PIXEL else (lm.y * w) for lm in landmarks)
                    y_min, y_max = self._find_min_max(y_vals)

                    box_w, box_h = x_max - x_min, y_max - y_min
                    bbox = x_min, y_min, box_w, box_w

                    if self.include_box:
                        hand_data.append(bbox)
                    if self.include_center:
                        cx, cy = bbox[0] + (bbox[2] / 2), bbox[1] + (bbox[3] / 2)
                        hand_data.append((cx, cy))

                hand_data.append(lm_list)

                if self.coordinates == CoordinatesType.PIXEL and self.draw_hand:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                    if self.include_box:
                        pass
                        # cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 255), 2)

        return hand_data, img

    def _calc_landmark_list(self, lm_list):
        if lm_list is None:
            return []
        elif not lm_list:
            return [lm for lm in range(0, 21)]
        else:
            return lm_list

    def _find_min_max(self, lm_vals):
        min_val = math.inf
        max_val = -math.inf
        for v in lm_vals:
            if v > max_val:
                max_val = v
            if v < min_val:
                min_val = v
        return min_val, max_val
