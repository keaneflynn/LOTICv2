import cv2
import numpy as np
import math  


class Detection:
    def __init__(self, class_id, score, box):
        self.class_id = class_id
        self.score = score
        self.box = box
        self.center = [(box[2] // 2 + box[0]),(box[3] // 2 + box[1])] 


def check_species(detected_species, score, species_dict):
    # species_dict = {class_id: [hits, average confidence]}

    if detected_species in species_dict.keys():
        hits = species_dict.get(detected_species)[0] + 1
        avg_conf = (species_dict.get(detected_species)[1] * (hits - 1) + score) / hits
        species_dict[detected_species] = [hits, avg_conf]
    else:
        species_dict[detected_species] = [1, score]

    if len(species_dict) == 1:
        return detected_species, species_dict
    else:
        spec_max = 0
        species = None
        for k, v in species_dict.items():
            if v[1] > spec_max:
                species = k
                spec_max = v[1]
    return species, species_dict


def get_length_cm(center, depth_f, box_width, frame_width):
    center_tup = (center[0], center[1]) 
    distance_mm = depth_f[center_tup]
    return ((distance_mm * box_width * 2.45) / (1.93 * frame_width)) / 10 #parameters for intel RealSense d435 camera unit


def update_length_list(center, depth_f, box_width, frame_width, length_list):
    len_cm = get_length_cm(center, depth_f, box_width, frame_width) 
    if len_cm < 0.1:
        pass
    elif (0.25 * frame_width) < center[0] < (0.75 * frame_width): 
        length_list[0].append(len_cm)
        length_list[0].sort()
        length_list[1].append(len_cm)
        length_list[1].sort()
    else:
        length_list[0].append(len_cm)
        length_list[0].sort()
    return length_list


class Fish:
    id_count = 0

    def __init__(self, class_id, score, box, frame, depth, frame_width):
        self.fish_id = Fish.id_count
        Fish.id_count += 1
        self.class_id = class_id
        self.hits_dict = {class_id: [1, score]}
        self.box = box
        self.center = [(box[2] // 2 + box[0]),(box[3] // 2 + box[1])]
        self.max_confidence = score
        self.score = score
        self.max_c_frame = frame
        self.hit_streak = 0
        self.frames_without_hit = 0
        self.first_center = [(box[2] // 2 + box[0]),(box[3] // 2 + box[1])]
        # length_list in the format [[list of all length measurements],
        #                           [list of length measurements where center x in center of frame]]
        self.length_list = [[], []]
        self.length_list = update_length_list([(box[3] // 2 + box[1]), (box[2] // 2 + box[0])], depth, box[2], frame_width, self.length_list) #rs center coordinate system (y,x)

    def update_fish(self, box, score, frame, class_id, depth, frame_width):
        # updates state of tracked objects
        self.hit_streak += 1
        self.box = box
        self.center = [(box[2] // 2 + box[0]),(box[3] // 2 + box[1])]
        self.frames_without_hit = 0
        self.class_id, self.hits_dict = check_species(class_id, score, self.hits_dict)
        self.length_list = update_length_list([(box[3] // 2 + box[1]), (box[2] // 2 + box[0])], depth, box[2], frame_width, self.length_list) #rs center coordinate system (y,x)

        if score > self.max_confidence:
            self.max_confidence = score
            self.max_c_frame = frame

    def predict(self):
        # checks if hitstreak needs to be reset
        # updates frames without hit
        # returns predicted location
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


def evaluate_length(len_list):
    # if more than 6 measurements are taken in center frame, return 80% median measurement
    if len(len_list[1]) >= 7:
        return len_list[1][len(len_list[1]) * 2 // 5] # * 4 originally
    else:
        return len_list[0][len(len_list[0]) * 4 // 5] # * 4 originally


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

    def update_tracker(self, classes, scores, boxes, frame, depth, frame_width):
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
            c = dets[m[1]].class_id
            self.tracked_objects[m[0]].update_fish(b, s, frame, c, depth, frame_width)

        # initialize new fish for unmatched detections and append to tracked_objects
        for u in umd:
            new_fish = Fish(dets[u].class_id, dets[u].score, dets[u].box, frame, depth, frame_width)
            self.tracked_objects.append(new_fish)

        ret = []
        evicted = []

        # filter out dead tracked items, append ret with passing tracked_objects, and return ret
        for obj in self.tracked_objects:
            if obj.frames_without_hit >= self.max_age:
                self.tracked_objects.remove(obj) # removes individuals who timeout the object tracker criteria

            if (obj.hit_streak >= self.min_hits) and (obj.frames_without_hit >= self.max_age): # expels information on individuals no longer being considered in tracking algorithm
                evicted.append(obj)

            if (obj.frames_without_hit < 1) and (obj.hit_streak >= self.min_hits or self.frame_count <= self.min_hits): # main return for currently tracked individuals
                r = [obj.fish_id, obj.class_id, obj.max_confidence, obj.box]
                ret.append(r)

        if len(ret) == 0:
            return np.empty((0, 4)), evicted
        return ret, evicted

    '''
    def update_tracker_rs(self, classes, scores, boxes, frame, depth, frame_width):
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
            c = dets[m[1]].class_id
            self.tracked_objects[m[0]].update_fish(b, s, frame, c, depth, frame_width)

        # initialize new fish for unmatched detections and append to tracked_objects
        for u in umd:
            new_fish = Fish(dets[u].class_id, dets[u].score, dets[u].box, frame, depth, frame_width)
            self.tracked_objects.append(new_fish)

        ret = []
        evicted = []

        # filter out dead tracked items, append ret with passing tracked_objects, and return ret
        for obj in self.tracked_objects:
            if obj.frames_without_hit >= self.max_age:
                self.tracked_objects.remove(obj) # removes individuals who timeout the object tracker criteria

            if (obj.hit_streak >= self.min_hits) and (obj.frames_without_hit >= self.max_age): # expels information on individuals no longer being considered in tracking algorithm
                evicted.append(obj)

            if (obj.frames_without_hit < 1) and (obj.hit_streak >= self.min_hits or self.frame_count <= self.min_hits): # main return for currently tracked individuals
                r = [obj.fish_id, obj.class_id, obj.max_confidence, obj.box]
                ret.append(r)

        if len(ret) == 0:
            return np.empty((0, 4)), evicted
        return ret, evicted
    '''

class direction:
    # Uses half way marker from video input to identify direction of travel based on first location of evicted fish and last location of evicted fish
    # 4 potential returns are: Downstream movement, Upstream movement, milling: US to US, milling: DS to DS
    # Could potentially use difference between first and last detection location, however that might create an issue depending upon detection locations
    # There is potential here to improve the algorithm depending upon tracker and neural network efficacy
    def directionOutput(evicted_fish, camera_stream_side, frame_width):
        directions = []
        for fish in evicted_fish:
            if camera_stream_side == 'RR':
                if (fish.first_center[0] < frame_width / 2) and (fish.center[0] >= frame_width / 2):
                    travel_direction = 'downstream'
                elif (fish.first_center[0] > frame_width / 2) and (fish.center[0] <= frame_width / 2):
                    travel_direction = 'upstream'
                elif (fish.first_center[0] < frame_width / 2) and (fish.center[0] <= frame_width / 2):
                    travel_direction = 'mill: remained upstream'
                else:
                    travel_direction = 'mill: remained downstream'

            else:  # camera_stream_side == 'RL'
                if (fish.first_center[0] < frame_width / 2) and (fish.center[0] >= frame_width / 2):
                    travel_direction = 'upstream'
                elif (fish.first_center[0] > frame_width / 2) and (fish.center[0] <= frame_width / 2):
                    travel_direction = 'downstream'
                elif (fish.first_center[0] < frame_width / 2) and (fish.center[0] <= frame_width / 2):
                    travel_direction = 'mill: remained downstream'
                else:
                    travel_direction = 'mill: remained upstream'
            directions.append(travel_direction)
        return directions


class measure:
    def grabLength(evicted_fish):
        lengths = []
        for fish in evicted_fish:
            lengths.append(evaluate_length(fish.length_list))
        return lengths
