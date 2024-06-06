import cv2
from datetime import datetime

class Webcam():
    def __init__(self):
        url = "rtmp://103.130.211.150:10050/stream"
        self.vid = cv2.VideoCapture(url)
        # self.vid = cv2.VideoCapture(1)
    def get_frame(self):
        while True:
            _, img =  self.vid.read()
            # font
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # org = (50, 50)
            # fontScale = 1
            # color = (255, 0, 0)
            # thickness = 2

            # img = cv2.putText(img, datetime.now().strftime("%H:%M:%S"), org, font,
            #                     fontScale, color, thickness, cv2.LINE_AA)

            # yield cv2.imencode('.jpg', img)[1].tobytes()#frame

            yield img