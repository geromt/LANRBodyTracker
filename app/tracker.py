import itertools

import cv2
import socket
from cvzone.HandTrackingModule import HandDetector


class HandTracker:
    def __init__(self, width: int = 1280, height: int = 720, port: int = 5052):
        """

        :param width: Ancho de la imagen capturada por la webcam
        :param height: Alto de la imagen capturada por la webcam
        :param port: Puerto por el que se mandan los datos capturados. Default: 5052
        """
        self.height = height
        self.width = width
        self.port = port

        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, self.width)
        self.capture.set(4, self.height)


        # Solo detecta una mano, la primera que aparece frente a la webcam. Es posible detectar más de una.
        self.detector = HandDetector(maxHands=2, detectionCon=0.8)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address_port = ("127.0.0.1", self.port)

    def _process_capture(self):
        success, img = self.capture.read()

        if not success:
            return

        hands, img = self.detector.findHands(img)
        data = []
        for hand in hands:
            landmarks = hand["lmList"]
            hand_type = hand["type"]
            data.append(hand_type)
            data.append(img.shape[0])
            data.append(img.shape[1])
            data.extend(itertools.chain(*landmarks))
        if not hands:
            data.append("NoHand")

        return img, data

    def capture_and_send(self, display_video: bool = False):
        """
        Captura los movimientos de la mano y manda los datos por el puerto especificado. Para conocer la estructura de
        los datos revisar README.md

        :param display_video: Muestra la captura de la webcam
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while True:
                img, data = self._process_capture()
                if data:
                    s.sendto(str.encode(str(data)), self.server_address_port)

                if display_video:
                    img = cv2.resize(img, (self.width, self.height))
                    cv2.imshow("Image", img)
                    cv2.waitKey(1)
