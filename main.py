from argparse import ArgumentParser
from neuralNet import *


def main():
    parser = ArgumentParser(description='LOTICv2')
    parser.add_argument('VideoSource', type=str, help='identify your video source i.e. IP camera source')
    parser.add_argument('WeightsFile', type=str, help='YOLO weight file')
    parser.add_argument('ConfigFile', type=str, help='YOLO configuration file')
    parser.add_argument('NamesFile', type=str, help='YOLO class names file')
    parser.add_argument('SiteCode', type=str, help='Site location ex) WillowCreek')
    parser.add_argument('StreamSide', type=str, default='RR', help='river right (RR) or river left (RL)')
    parser.add_argument('ConfigFile', type=str, help='YOLO configuration file')
    parser.add_argument('ConfidenceActivation', type=float, default=0.2, help='confidence threshold to activate main loop')
    parser.add_argument('ExitThreshold', type=int, help='Seconds after leaving screen to disable main loop')
    parser.add_argument('MediaOutput', type=str, default='image', help='image or video output (note video output will bog down throughput')
    args = parser.parse_args()
    
    od = objectDetection()
    od.loadNN(args)

    while cv2.waitKey(1) < 1:
        frameImport()
        od.detection()
        objectTracker()
        etc . . .

if __name__ == '__main__':
    main()

