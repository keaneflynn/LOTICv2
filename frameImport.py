import cv2
import queue

class frameImport:
    def __init__(self, video_input):
        self.video_input = video_input
        self.frame_input_queue = queue.Queue(100)

    def videoSource(self):
        self.video_source = cv2.VideoCapture(self.video_input)
        return self.video_source

    def receiveFrame(self):
        while True:
            grabbed, self.frame = self.video_source.read()
            self.frame_input_queue.put(self.frame)

    def grabFrame(self):
        return self.frame_input_queue.get()
