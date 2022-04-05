from math import floor
import signal
import threading
import cv2

from argparse import ArgumentParser
from objectDetection import objectDetection, outputTesting #Remove testing for final script
from frameImport import *
from objectTracker import objectTracker, direction
from output import videoOutput
from lotic_signal import LoticSignal

def main():
    parser = ArgumentParser(description='LOTICv2')
    parser.add_argument('video_source', type=str, help='identify your video source, using "realsense" will result in use with realsense camera')
    parser.add_argument('weights_file', type=str, help='YOLO weight file')
    parser.add_argument('config_file', type=str, help='YOLO configuration file')
    parser.add_argument('names_file', type=str, help='YOLO class names file')
    parser.add_argument('site_code', type=str, help='Site location ex) WillowCreek')
    parser.add_argument('stream_side', type=str, default='RR', help='river right (RR) or river left (RL)')
    parser.add_argument('nn_confidence_activation', type=float, default=0.25, help='confidence threshold to activate main loop')
    parser.add_argument('video_exit_threshold', type=int, default = 7, help='Seconds after leaving screen to disable detection loop for detected fishes')
    parser.add_argument('output_file_directory', type=str, default='./outfile/', help='json and video file output storage location')
    parser.add_argument('--output_with_bounding_boxes', type=str, default='no', help='enter either yes or no to add bounding boxes to video output')
    args = parser.parse_args()

    ls = LoticSignal()
    signal.signal(signal.SIGINT, ls.handler)

    od = objectDetection(args.nn_confidence_activation,
                         args.weights_file,
                         args.config_file,
                         args.names_file) #initialize class list and model params
    od.loadNN() #initializes the parameters for which the neural network needs to run (these are optimized for nvidia jetson w/CUDA)

    if args.video_source == 'realsense': #still needs updates to work with realsense camera, will focus on this later
        from realsense import realsense
        from output import jsonOut_rs
        jo = jsonOut_rs()
        rs = realsense()
        video_info = [rs.getFPS(),
                      rs.getFrameWidth(),
                      rs.getFrameHeight()]

    else:
        from output import jsonOut
        jo = jsonOut(args.site_code, args.names_file, args.output_file_directory)
        fi = frameImport(0, ls) #args.video_source #takes in args flag for video source and creates pipeline for frame import
        color_frame = fi.videoSource() #frame source
        video_info = [color_frame.get(cv2.CAP_PROP_FPS), #for use with IP cameras, it may be necessary to hardcode in your FPS since OpenCV has issues decyphering this value
                      color_frame.get(cv2.CAP_PROP_FRAME_WIDTH),
                      color_frame.get(cv2.CAP_PROP_FRAME_HEIGHT)]

    t1 = threading.Thread(target=fi.receiveFrame)
    t1.start()

    vo = videoOutput(args.site_code, args.video_exit_threshold, video_info, args.output_file_directory)

    #These are the only global variables that will likely have to be adjusted for specific use cases (depend on fish speed, model accuracy, etc.)
    max_tracker_age = floor(video_info[0]) * 3 #takes 3 seconds for program to evict a tracked individual
    min_tracker_hits = 2 #needs 2 detections to initialize tracker for an individual
    min_pixel_distance = video_info[1]/3 #after traveling 33% of the width of the screen in pixels, the tracker will evict the tracked individual

    ot = objectTracker(max_tracker_age, min_tracker_hits, min_pixel_distance)


    while ls.keep_running():
        if args.video_source == 'realsense': #Current variable name for testing only
            grabbed, depth_frame, frame = rs.grab_frame()
        else:
            frame = fi.grabFrame() #Imports frame from video source 
            if frame is None:
                break


        classes, scores, boxes = od.detection(frame) #performs object detection on individual frame from method in cv2 library
        

        tracked_fish, evicted_fish = ot.update_tracker(classes, scores, boxes, frame) #object tracker (shoutout Jack) that updates output from object detection and can track individuals across a series of frames 
        
    
        travel_direction = direction.directionOutput(evicted_fish, args.stream_side, video_info[1]) #returns the direction of travel for "evicted fish" informed by object tracker


        jo.writeFile(evicted_fish, travel_direction) #when a fish is declared "evicted". all relevant information from that individual will be included in a .json file that is output

        
        vo.writeVideo(tracked_fish, frame) #when fish are absent from the video frame for a specified amount of time, an .avi file will be written out for all frames containing the fish


        if args.output_with_bounding_boxes == 'yes':
            oTest = outputTesting(args.names_file) #remove for actual script
            oTest.testOutputFrames(frame, tracked_fish) #remove for actual script

    t1.join()


if __name__ == '__main__':
    main()
