import numpy as np
import cv2


def run():
    capture = cv2.VideoCapture("rtsp://admin:viet29@viet@192.168.1.2:554/onvif1", cv2.CAP_FFMPEG)
    while True:
        result, frame = capture.read()
        cv2.imshow('video', frame)

        if cv2.waitKey(16) == ord("q"):
            break