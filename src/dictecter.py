from ultralytics import YOLO
import cv2
from datetime import datetime 
class DITECTERS:
    def __init__(self):
        self.url =  f"rtsp://admin:aarush252011%21@192.168.1.98:554/Streaming/Tracks/101?starttime=20260529T121000Z&endtime=20260529T122000Z"
    def ditec(self):
        cam = cv2.VideoCapture(self.url)
        while True:
            ret, frame = cam.read()
            if not ret:
                print('OOP!')
            cv2.imshow('ditec',frame)
            if cv2.waitKey(1) == ord('a'):
                break
        cam.release()
        cv2.destroyAllWindows()
cam = DITECTERS()
cam.ditec()
