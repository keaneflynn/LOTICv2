import cv2

class objectDetection:
    def __init__(self):
        self.confidence = 0.5
        self.nmsThreshold = 0.1
        self.colors = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]

        class_names = []
        with open("models/coco.names", "r") as f:
            class_names = [cname.strip() for cname in f.readlines()]

    def loadNN(self):
        #vc = cv2.VideoCapture('rtsp://admin:admin123456@192.168.1.12:554') #for use with IP camera

        net = cv2.dnn.readNet("models/yolov4-tiny.weights", "models/yolov4-tiny.cfg")
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA) #must be enabled for GPU use
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16) #reduced latency nn processing, slight hit on accuracy
        #net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA) #higher accuracy target use

        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

    def detection(self):
        classes, scores, boxes = model.detect(frame, self.confidence, self.nmsThreshold)
