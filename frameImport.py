import cv2

class frameImport:
    def __init__(self, video_input):
        self.video_input = video_input

    def loadFrame(self):
        color_frame = cv2.VideoCapture(self.video_input)
        return color_frame

    def loadFrame_rs(self):
        from realsense import realsense
        rs = realsense()
        ret, depth_frame, color_frame = rs.grab_frame() #pulls info from intel camera (we are interested in the color_frame)
        return ret, depth_frame, color_frame