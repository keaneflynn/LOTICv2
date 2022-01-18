import cv2
import numpy as np
import math #needed for math.hypot (needed for comparing objects between frames)

class Detection:
    def __init__(self, class_id, score, box):
        self.class_id = class_id
        self.score = score
        self.center = [box[0], box[1]]


class Fish:
    id_count = 0

    def __init__(self, class_id, score, box, frame):
        self.fish_id = Fish.id_count
        Fish.id_count += 1
        self.class_id = class_id
        self.box = box
        self.center = [box[0], box[1]]
        self.max_confidence = score
        self.max_c_frame = frame
        self.hit_streak = 0
        self.frames_without_hit = 0

    def update_fish(self, box, score, frame):
        #updates state of tracked objects
        self.hit_streak += 1
        self.center = [box[0], box[1]]
        self.frames_without_hit = 0
        if score > self.max_confidence:
            self.max_confidence = score
            self.max_c_frame = frame

    def predict(self):
        #checks if hitstreak needs to be reset
        #updates frames without hit
        #returns predicted location
        if self.frames_without_hit > 0:
            self.hit_streak = 0
        self.frames_without_hit += 1
        # return self.center


def dist(center1, center2):
    return math.hypot(center1[0] - center2[0], center1[1] - center2[1])


class objectTracker:

    def __init__(self, stream_side, exit_threshold=2, min_hits=3, min_distance=0.06):
        self.stream_side = stream_side
        self.max_age = exit_threshold
        self.min_hits = min_hits
        self.min_distance = min_distance
        self.tracked_objects = []
        self.frame_count = 0

    def update_tracker(self, classes, scores, boxes, frame):
        self.frame_count += 1
        # ret = list of tracked_objects that pass min_hits and max_age filter in the form
        # [fish_id, class_id, score, box]
        ret = []

        # predict called first, update_fish called next
        # predicts current frame location of tracked_objects using previous frame information
        predicted_center_points = []
        for t in self.tracked_objects:
            t.predict()
            predicted_center_points.append(t.center)

        # format detections
        dets = []
        dets_center_points = []
        for c, s, b in zip(classes, scores, boxes):
            det = Detection(c, s, b)
            dets.append(det)
            dets_center_points.append(det.center)

        # check associations: given predicted_center_points and dets_center_points return matches,  in the form of a
        # 2d array with shape(n, 2) where column 0 = index in tracked items and column 1 = index in dets

        # handling matches - don't create new tracklet, update tracklet position do it in the double loop




        # update all tracked_objects in matches with respective detections

        # initialize new fish for unmatched detections and append to tracked_objects

        # filter out dead tracked items - happens by evaluating fish.frames_without_update - predict is called on all
        # tracked objects by update is only called on matches

        # append ret with passing tracked_objects and return ret

        return ret



#    def tracker(self):
#
#    def classLock(self):
#
#    def maxConf(self):
#
#    def travelDirection(self):
#
#    def objectLength(self): #Keane project for realsense shit
