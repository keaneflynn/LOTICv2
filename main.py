from math import floor
import cv2
import multiprocessing as mp

from argparse import ArgumentParser
from objectDetection import objectDetection, outputTesting #Remove testing for final script
from frameImport import *
from objectTracker import objectTracker, direction
from output import jsonOut, videoOutput


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
    parser.add_argument('exit_threshold', type=int, help='Seconds after leaving screen to disable detection loop for detected fishes')
    parser.add_argument('media_output', type=str, default='image', help='image or video output (note video output will bog down throughput')
    args = parser.parse_args()
    
    od = objectDetection(args.confidence_activation,
                         args.weights_file,
                         args.config_file,
                         args.names_file) #initialize class list and model params
    vo = videoOutput(args.exit_threshold)

    if args.video_source == 'realsense':
        from realsense import realsense
        from objectTracker import depthMapping
        from output import jsonOut_rs
        jo = jsonOut_rs()
        dm = depthMapping()
        rs = realsense()
        video_info = [rs.getFPS(),
                      rs.getFrameWidth()
                      rs.getFrameHeight()]

    else:
        from output import jsonOut
        jo = jsonOut()
        fi = frameImport(args.video_source) #takes in args flag for video source and creates pipeline for frame import
        color_frame = fi.loadFrame() #frame source
        video_info = [color_frame.get(cv2.CAP_PROP_FPS),
                      color_frame.get(cv2.CAP_PROP_FRAME_WIDTH),
                      color_frame.get(cv2.CAP_PROP_FRAME_HEIGHT)]

    od.loadNN()
    vo = videoOutput(args.sitecode, args.exit_threshold, video_info)

    max_tracker_age = floor(fps)/1
    min_tracker_hits = 2
    min_pixel_distance = frame_width/5 

    ot = objectTracker(max_tracker_age, min_tracker_hits, min_pixel_distance)
    dir = direction(max_tracker_age)
    '''

    # tracker testing w hardcoded variables

    confidence = 0.25
    weights = "models/yolov4-tiny-fish.weights"
    config = "models/yolov4-tiny-fish.cfg"
    name = "models/yolov4-tiny-fish.names"
    vid = "media/coho-steelhead-test-short.mov"
    camera_stream_side = 'RR'
    sitename = 'testSite'
    output_directory = './outfile/'

    od = objectDetection(confidence, weights, config, name)
    fi = frameImport(vid)
    jo = jsonOut(sitename, name)
    color_frame = fi.loadFrame()
    video_info = [color_frame.get(cv2.CAP_PROP_FPS),
                  color_frame.get(cv2.CAP_PROP_FRAME_WIDTH),
                  color_frame.get(cv2.CAP_PROP_FRAME_HEIGHT)]

    od.loadNN()
    vo = videoOutput(sitename, 2, video_info)

    # below are optimal tracker parameters for fish model and test video
    max_tracker_age = floor(video_info[0]) * 3 #where integer is number of seconds to break tracker 
    min_tracker_hits = 2 #2 for testing
    min_pixel_distance = video_info[1]/5 #20% of frame width #270 for testing
    ot = objectTracker(max_tracker_age, min_tracker_hits, min_pixel_distance)

    while cv2.waitKey(1):
        if vid == 'realsense': #if args.video_source == 'realsense':# #Current variable name for testing only
            grabbed, depth_frame, frame = rs.grab_frame()
        else:
            grabbed, frame = color_frame.read() #add multithreading
        if not grabbed:
            exit(0)


        classes, scores, boxes = od.detection(frame)


        # tracked_fish = 2d list shape(n, 4) of tracked objects in the format [fish_id, class, score, box]
        tracked_fish, evicted_fish = ot.update_tracker(classes, scores, boxes, frame)
        
    
        travel_direction = direction.directionOutput(evicted_fish, camera_stream_side, video_info[1])


        jo.writeFile(evicted_fish, travel_direction, output_directory) #comment out to stop json output

    
        vo.writeVideo(tracked_fish, frame)

        ''' 
        test stuff
        tf = []
        for i in tracked_fish:
            tf.append(i[0])

        print(tf)
        print(tracklets)
        print("/n")    
        '''

        oTest = outputTesting(name) #remove for actual script
        oTest.testOutputFrames2(frame, tracked_fish) #remove for actual script


if __name__ == '__main__':
    main()

