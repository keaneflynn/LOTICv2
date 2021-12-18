from argparse import argparser
from neuralNet import *


def main():
    nn = neuralNet()

    while cv2.waitKey(1) < 1:
        frameImport()
        inference()
        objectTracker()
        etc . . .

if __name__ == '__main__':
    main()

