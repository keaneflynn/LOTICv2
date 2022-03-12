import pyrealsense2 as rs
import numpy as np

print("hello")

class realsense:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.fps = 30
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, self.fps)
        config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, self.fps)
        self.pipeline.start(config)

    def getFPS(self):
        return self.fps

    def getFrameWidth(self):
        return self.width

    def getFrameHeight(self):
        return self.height

    def grab_frame(self):
        frame = self.pipeline.wait_for_frames()
        depth_frame = frame.get_depth_frame()
        color_frame = frame.get_color_frame()
        depth_frame = np.asanyarray(depth_frame.get_data())
        color_frame = np.asanyarray(color_frame.get_data())
        if depth_frame is None or color_frame is None:
            print("No frames detected, check camera connection")
            exit(1)
        return True, depth_frame, color_frame
    
    def release_frame(self):
        self.pipeline.stop()
