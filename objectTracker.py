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
        self.first_center = [box[0], box[1]]
    

    def update_fish(self, box, score, frame):
        #updates state of tracked objects
        self.hit_streak += 1
        self.box = box
        self.center = [box[0], box[1]]
        self.frames_without_hit = 0
        if score > self.max_confidence:
            self.max_confidence = score
            self.max_c_frame = frame

    def predict(self):
        #checks if hitstreak needs to be reset
        #updates frames without hit
        #returns predicted location
        # if self.frames_without_hit > 4:
         #   self.hit_streak = 0
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

    def __init__(self, exit_threshold, min_hits, min_distance):
        # self.stream_side = stream_side
        self.max_age = exit_threshold
        self.min_hits = min_hits
        self.min_distance = min_distance
        # list of Fish objects detected
        self.tracked_objects = []
        self.frame_count = 0
        # list of final objects tracked in the form [fish_id, class_id, score, box]


    def update_tracker(self, classes, scores, boxes, frame):
        self.frame_count += 1

        # predicts current frame location of tracked_objects using previous frame information
        predicted_center_points = []
        to_ind = np.arange(len(self.tracked_objects))
        for t in to_ind:
            self.tracked_objects[t].predict()
            predicted_center_points.append(self.tracked_objects[t].center)

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
            b = dets[m[1]].box
            s = dets[m[1]].score
            self.tracked_objects[m[0]].update_fish(b, s, frame)

        # initialize new fish for unmatched detections and append to tracked_objects
        for u in umd:
            new_fish = Fish(dets[u].class_id, dets[u].score, dets[u].box, frame)
            self.tracked_objects.append(new_fish)

        ret = []
        evicted = []

        # filter out dead tracked items, append ret with passing tracked_objects, and return ret
        for obj in self.tracked_objects:
            if obj.frames_without_hit >= self.max_age:
                self.tracked_objects.remove(obj)
                #e = [obj.fish_id, obj.first_center, obj.center]
                #evicted.append(e)
                evicted.append(obj)
                continue

            if (obj.frames_without_hit < 1) and (obj.hit_streak >= self.min_hits or self.frame_count <= self.min_hits):
                r = [obj.fish_id, obj.class_id, obj.max_confidence, obj.box]
                ret.append(r)

        if len(ret) == 0:
            return np.empty((0,4)), evicted
        return ret, evicted


class direction:
    #Uses half way marker from video input to identify direction of travel based on first location of evicted fish and last location of evicted fish
    #4 potential returns are: Downstream movement, Upstream movement, milling: US to US, milling: DS to DS
    #Could potentially use difference between first and last detection location, however that might create an issue depending upon detection locations
    #There is potential here to improve the algorithm depending upon tracker and neural network efficacy
    def directionOutput(evicted_fish, camera_stream_side, frame_width):
        for fish in evicted_fish:
            if camera_stream_side == 'RR':
                if fish.first_center[0] < frame_width/2 and fish.center[0] >= frame_width/2:
                    travel_direction = 'downstream'
                elif fish.first_center[0] > frame_width/2 and fish.center[0] <= frame_width/2: 
                    travel_direction = 'upstream'
                elif fish.first_center[0] < frame_width/2 and fish.center[0] <= frame_width/2:
                    travel_direction = 'mill: remained upstream'
                else:
                    travel_direction = 'mill: remained downstream'

            else: #camera_stream_side == 'RL'
                if fish.first_center[0] < frame_width/2 and fish.center[0] >= frame_width/2:
                    travel_direction = 'upstream'
                elif fish.first_center[0] > frame_width/2 and fish.center[0] <= frame_width/2: 
                    travel_direction = 'downstream'
                elif fish.first_center[0] < frame_width/2 and fish.center[0] <= frame_width/2:
                    travel_direction = 'mill: remained downstream'
                else:
                    travel_direction = 'mill: remained upstream'

            return travel_direction


class depthMapping:
    def __init__(self):
        self.sensor_width_mm = 3.60
        self.sensor_height_mm = 2.10
        self.focal_length = 1.88
        self.image_width_pixels = 1280
        self.image_height_pixels = 720

        self.frameDetection_lengths = []

    def getLengths(self, depth_frame, tracked_fish):
        self.depth_frame = depth_frame
        self.tracked_fish = tracked_fish
        center_points = []
        object_depth = []
        box_width = [] #figure this out tomorrow
        for tf in self.tracked_fish:
            center_points = (tf[3][1], tf[3][0])
            #box_width = #figure this out tomorrow
            object_depth = self.depth_frame[center_points]
            object_length = self.frameDetection_lengths.append((object_depth[tf] * self.box_width[tf] * self.sensor_width_mm) / (self.focal_length * self.image_width_pixels))
            
            #frameDetection_lengths.append = self.depth_frame[self.center[tf[0]]]
        return object_length

    def updateAverageLength(self):
        ###Use time to set breakout threshold. If theshold is exceeded then break function###
        self.objectLengths = getLenths()
        
