import cv2
from realsense import realsense

class frameImport:
    def __init__(self, video_input):
        self.video_input = video_input

    def loadFrame(self):
        #Condition for grabbing frames from Intel RealSense camera
        if self.video_input == 'realsense':
            rs = realsense()
            ret, depth_frame, color_frame = rs.grab_frame() #pulls info from intel camera (we are interested in the color_frame)          
        else:       
            color_frame = cv2.VideoCapture(self.video_input)

        return color_frame
