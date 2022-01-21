import cv2
import numpy as np
import math #needed for math.hypot (needed for comparing objects between frames)

class Detection:
    def __init__(self, class_id, score, box):
        self.class_id = class_id
        self.score = score
        self.box = box
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
        self.score = score
        self.max_c_frame = frame
        self.hit_streak = 0
        self.frames_without_hit = 0

    def update_fish(self, center, score, frame):
        #updates state of tracked objects
        self.hit_streak += 1
        self.center = center
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


def distance(center1, center2):
    return math.hypot(center1[0] - center2[0], center1[1] - center2[1])


def association(tracks, detections, min_distance):
    if len(tracks) == 0:
        return np.empty((0, 2), dtype=int), np.arange(len(detections))

    dets = []
    ls = np.arange(len(detections))
    for i, de in zip(ls, detections):
        dets.append([i, de])

    matched_indices = []
    for t, trk in enumerate(tracks):
        for d in dets:
            dist = distance(trk, d[1])
            if dist <= min_distance:
                matched_indices.append([t, d[0]])
                dets.remove(d)
                break

    unmatched_detection_indices = []
    for i in dets:
        unmatched_detection_indices.append(i[0])

    return matched_indices, unmatched_detection_indices


class objectTracker:

    def __init__(self, stream_side, exit_threshold=2, min_hits=3, min_distance=0.06):
        self.stream_side = stream_side
        self.max_age = exit_threshold
        self.min_hits = min_hits
        self.min_distance = min_distance
        # list of Fish objects detected
        self.tracked_objects = []
        self.frame_count = 0
        # list of final objects tracked in the form [fish_id, class_id, score, box]
        # self.frame_final_objects = []

    def update_tracker(self, classes, scores, boxes, frame):
        self.frame_count += 1

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

        # association: given predicted_center_points and dets_center_points return matches, a
        # 2d list with shape(n, 2) where each row represents a match, column 0 = index in tracked_objects, and
        # column 1 = index in dets, and unmatched detections a
        matches, umd = association(predicted_center_points, dets_center_points, self.min_distance)

        # update all tracked_objects in matches with respective detections
        for m in matches:
            c = dets[m[1]].center
            s = dets[m[1]].score
            self.tracked_objects[m[0]].update_fish(c, s, frame)

        # initialize new fish for unmatched detections and append to tracked_objects
        for u in umd:
            new_fish = Fish(dets[u].class_id, dets[u].score, dets[u].box, frame)
            self.tracked_objects.append(new_fish)

        ret = []
        # self.frame_final_objects = []
        # filter out dead tracked items, append ret with passing tracked_objects, and return ret
        for obj in self.tracked_objects:
            if obj.frames_without_hit >= self.max_age:
                self.tracked_objects.pop(obj)
            if (obj.frames_without_hit < 1) and (obj.hit_streak >= self.min_hits or self.frame_count <= self.min_hits):
                r = [obj.fish_id, obj.class_id, obj.score, obj.box]
                ret.append(r)

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
