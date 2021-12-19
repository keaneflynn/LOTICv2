import cv2

class neuralNet:
    def __init__(self):
        CONFIDENCE_THRESHOLD = 0.5
        NMS_THRESHOLD = 0.1
        COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

        class_names = []
        with open("models/coco.names", "r") as f:
            class_names = [cname.strip() for cname in f.readlines()]

        vc = cv2.VideoCapture('rtsp://admin:admin123456@192.168.1.12:554') #for use with IP camera
        #vc = cv2.VideoCapture('test.mp4')

        #net = cv2.dnn.readNet("models/yolov4.weights", "models/yolov4.cfg")
        net = cv2.dnn.readNet("models/yolov4-tiny.weights", "models/yolov4-tiny.cfg")

        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA) #must be enabled for GPU use
        #net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16) #higher accuracy target use
        #net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA) #reduced latency nn processing, slight hit on accuracy

        #net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV) #must be enabled for CPU
        #net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU) #default processing target

        model = cv2.dnn_DetectionModel(net)
        #model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)
        model.setInputParams(size=(416, 416), scale=1/float(255.0), swapRB=True) #float is important for Python version 2!!!
