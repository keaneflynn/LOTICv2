import cv2
import multiprocessing as mp

from argparse import ArgumentParser
from objectDetection import objectDetection
from frameImport import frameImport
from objectTracker import objectTracker


def main():
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
    color_frame = fi.loadFrame()
    od.loadNN()

    while cv2.waitKey(1) < 1:
        grabbed, frame = color_frame.read() #add multithreading
        if not grabbed:
            break
        classes, scores, boxes = od.detection(frame)

        ot = objectTracker(args.stream_side)
        # tracked_fish = 2d list shape(n, 4) of tracked objects in the format [fish_id, class_id, score, box]
        tracked_fish = ot.update_tracker(classes, scores, boxes, frame)

        od.testOutputFrames(frame, classes, scores, boxes)

if __name__ == '__main__':
    main()

