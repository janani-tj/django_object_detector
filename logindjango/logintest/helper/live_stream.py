import threading
import cv2
class VideoCamera(object):
    def __init__(self):
        #print("here")
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
        #self.update()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        #print("here1")
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
