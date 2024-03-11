import math
import time

import cv2
import socket
import mediapipe as mp

from app.config_reader import ConfigReader, CoordinatesType


class BodyTracker:
    def __init__(self, config: ConfigReader):
        self.capture = cv2.VideoCapture(config.camera_index)
        self.port = config.port
        self.frame_height = config.frame_height
        self.frame_width = config.frame_width

        self.display_video = config.display_video
        self.display_video_size = config.display_video_size
        self.draw_pose = config.draw_pose
        self.mpDraw = mp.solutions.drawing_utils

        if config.config_frame:
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)

        self.mpPose = mp.solutions.pose
        self.detector = self.mpPose.Pose(static_image_mode=config.static_mode,
                                         smooth_landmarks=config.smooth_landmarks,
                                         model_complexity=config.model_complexity,
                                         enable_segmentation=config.enable_segmentation,
                                         smooth_segmentation=config.smooth_segmentation,
                                         min_detection_confidence=config.min_detection_confidence,
                                         min_tracking_confidence=config.min_tracking_confidence)

        self.server_address_port = ("127.0.0.1", self.port)
        self.count_frame = 0
        self.init_time = time.time()

        self.results = None
        self.include_fps = config.include_fps
        self.include_height = config.include_height
        self.include_width = config.include_width
        self.flip_x = config.flip_x
        self.flip_y = config.flip_y
        self.coordinates = config.coordinates
        self.lm_list = self._calc_landmark_list(config.lm_list)
        self.include_box = config.include_box
        self.include_center = config.include_center
        self.include_visibility = config.include_visibility
        self.round = config.round
        self.print_data = config.print_data

    def _process_capture(self):
        success, img = self.capture.read()

        if not success:
            return

        data, img = self.find_pose(img)
        if not data:
            data.append("")

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
                        int(self.frame_width * self.display_video_size),
                        int(self.frame_height * self.display_video_size)))
                    cv2.imshow("Image", img)
                    cv2.waitKey(1)

    def find_pose(self, img):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :return: Image with or without drawings
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.detector.process(img_rgb)
        body_data = []
        h, w, c = img.shape

        if self.coordinates == CoordinatesType.REAL_WORLD:
            pose_landmarks = self.results.pose_world_landmarks
        else:
            pose_landmarks = self.results.pose_landmarks

        if pose_landmarks:
            if self.include_fps:
                self.count_frame += 1
                body_data.append(int(self.count_frame / (time.time() - self.init_time)))

            if self.include_height:
                body_data.append(h)
            if self.include_width:
                body_data.append(w)

            lm_list = []

            for i, lm in enumerate(pose_landmarks.landmark):

                if self.coordinates == CoordinatesType.PIXEL:
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                else:
                    px, py, pz = lm.x, lm.y, lm.z

                if self.round >= 0:
                    px = round(px, self.round)
                    py = round(py, self.round)
                    pz = round(pz, self.round)

                if self.flip_y:
                    py = 1 - py
                    py = round(py, self.round)
                if self.flip_x:
                    px = 1 - px
                    px = round(px, self.round)

                if self.include_visibility:
                    lm_list.append(round(lm.visibility, self.round))

                lm_list.extend((px, py, pz))

            if self.include_box or self.include_center:
                x_vals = (lm.x if self.coordinates == CoordinatesType.PIXEL else (lm.x * w) for lm in pose_landmarks)
                x_min, x_max = self._find_min_max(x_vals)

                y_vals = (lm.y if self.coordinates == CoordinatesType.PIXEL else (lm.y * w) for lm in pose_landmarks)
                y_min, y_max = self._find_min_max(y_vals)

                if self.coordinates == CoordinatesType.PIXEL:
                    x_min = int(x_min * w)
                    x_max = int(x_max * w)
                    y_min = int(y_min * h)
                    y_max = int(y_max * h)

                box_w, box_h = x_max - x_min, y_max - y_min
                bbox = x_min, y_min, box_w, box_w

                if self.include_box:
                    body_data.extend(bbox)
                if self.include_center:
                    cx, cy = bbox[0] + (bbox[2] / 2), bbox[1] + (bbox[3] / 2)
                    body_data.extend((cx, cy))

            body_data.extend(lm_list)

            if self.coordinates == CoordinatesType.PIXEL and self.draw_pose:
                self.mpDraw.draw_landmarks(img, pose_landmarks, self.mpPose.POSE_CONNECTIONS)
                if self.include_box:
                    cv2.rectangle(img,
                                  (bbox[0], bbox[1]),
                                  (bbox[0] + bbox[2], bbox[1] + bbox[3]),
                                  (255, 0, 255),
                                  2)

        return body_data, img

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
