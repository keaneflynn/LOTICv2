import cv2
import numpy as mp
import math #needed for math.hypot (needed for comparing objects between frames)



class objectTracker:
    def __init__(self, frame, classes, scores, boxes, stream_side, exit_threshold):
        self.frame = frame
        self.classes = classes
        self.scores = scores
        self.boxes = boxes
        self.stream_side = stream_side
        self.exit_threshold = exit_threshold

#    def tracker(self):
#
#    def classLock(self):
#
#    def maxConf(self):
#
#    def travelDirection(self):
#
#    def objectLength(self): #Keane project for realsense shit
