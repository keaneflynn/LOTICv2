import cv2
import platform

class objectDetection:
    def __init__(self, confidence_activation, weights_file, config_file, names_file):
        self.confidence = confidence_activation
        self.nmsThreshold = 0.2
        self.color = (0, 255, 255)

        self.weights_file = weights_file
        self.config_file = config_file

        class_names = []
        with open(names_file, "r") as f:
            class_names = [cname.strip() for cname in f.readlines()]

    def loadNN(self):
        os_name = platform.system()
        net = cv2.dnn.readNet(self.weights_file, self.config_file)
        if os_name == 'Linux':
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA) #must be enabled for GPU use
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16) #reduced latency nn processing, slight hit on accuracy
            #net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA) #higher accuracy target use, slower
        else:
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV) #will target standard opencv build on Darwin and Windows 
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU) #CPU target, no GPU use. Slower, but for testing system

        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

    def detection(self, frame):
        classes, scores, boxes = self.model.detect(frame, self.confidence, self.nmsThreshold)
