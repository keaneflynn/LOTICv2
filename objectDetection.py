import cv2

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
        net = cv2.dnn.readNet(self.weights_file, self.config_file)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA) #must be enabled for GPU use
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16) #reduced latency nn processing, slight hit on accuracy
        #net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA) #higher accuracy target use, slower

        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

    def detection(self, frame):
        classes, scores, boxes = self.model.detect(frame, self.confidence, self.nmsThreshold)
