import cv2

class frameImport:
    def __init__(self, video_input):
        self.video_input = video_input

    def loadFrame(self):
        color_frame = cv2.VideoCapture(self.video_input)
        return color_frame
