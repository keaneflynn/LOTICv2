from math import floor
import cv2
import multiprocessing as mp

from argparse import ArgumentParser
from objectDetection import objectDetection
from frameImport import frameImport
from objectTracker import objectTracker


def main():
    '''
    parser = ArgumentParser(description='LOTICv2')
    parser.add_argument('video_source', type=str, help='identify your video source, using "realsense" will result in use with realsense camera')
    parser.add_argument('weights_file', type=str, help='YOLO weight file')
    parser.add_argument('config_file', type=str, help='YOLO configuration file')
    parser.add_argument('names_file', type=str, help='YOLO class names file')
    parser.add_argument('site_code', type=str, help='Site location ex) WillowCreek')
    parser.add_argument('stream_side', type=str, default='RR', help='river right (RR) or river left (RL)')
    parser.add_argument('confidence_activation', type=float, default=0.2, help='confidence threshold to activate main loop')
    parser.add_argument('exit_threshold', type=int, help='Seconds after leaving screen to disable main loop')
    parser.add_argument('media_output', type=str, default='image', help='image or video output (note video output will bog down throughput')
    args = parser.parse_args()
    
    od = objectDetection(args.confidence_activation,
                         args.weights_file,
                         args.config_file,
                         args.names_file) #initialize class list and model params
    fi = frameImport(args.video_source) #takes in args flag for video file and chooses between intel realsense camera
    if args.video_source == 'realsense':
        ret, depth_frame, color_frame = fi.loadFrame_rs()
    else:
        color_frame = fi.loadFrame()
    color_frame = fi.loadFrame()
    fps = video.get(cv2.CAP_PROP_FPS) #To be used to determine detection loop breaks    
    od.loadNN()
    '''

    # tracker testing w hardcoded variables

    confidence = 0.05
    weights = "models/yolov4-tiny-fish.weights"
    config = "models/yolov4-tiny-fish.cfg"
    name = "models/yolov4-tiny-fish.names"
    vid = "media/coho-steelhead-test-short.mov"

    od = objectDetection(confidence, weights, config, name)
    fi = frameImport(vid)
    color_frame = fi.loadFrame()
    fps = color_frame.get(cv2.CAP_PROP_FPS)
    od.loadNN()

    # below are optimal tracker parameters for fish model and test video
    max_tracker_age = floor(fps)/1 #where 1 is number of seconds# #26 for testing#
    min_tracker_hits = 2 #2 for testing
    min_pixel_distance = 270 #270 for testing
    ot = objectTracker(max_tracker_age, min_tracker_hits, min_pixel_distance)

    while cv2.waitKey(1) < 1:
        grabbed, frame = color_frame.read() #add multithreading
        if not grabbed:
            break
        classes, scores, boxes = od.detection(frame)

        # tracked_fish = 2d list shape(n, 4) of tracked objects in the format [fish_id, class, score, box]

        tracked_fish, tracklets = ot.update_tracker(classes, scores, boxes, frame)

        #dm = depthMapping(depth_frame, boxes, tracked_fish)
        #dm.grabForkLength()

        ''' 
        test stuff
        tf = []
        for i in tracked_fish:
            tf.append(i[0])

        print(tf)
        print(tracklets)
        print("/n")    
        '''

        od.testOutputFrames2(frame, tracked_fish)
        #print(tracklets)
        #print(tracked_fish)


if __name__ == '__main__':
    main()

