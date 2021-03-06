import cv2

class objectDetection:
    def __init__(self, confidence_activation, weights_file, config_file, names_file):
        self.confidence = confidence_activation
        self.nmsThreshold = 0.3

        self.weights_file = weights_file
        self.config_file = config_file

        self.class_names = []
        with open(names_file, "r") as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

    def loadNN(self):
        net = cv2.dnn.readNet(self.weights_file, self.config_file)
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA) #must be enabled for GPU use
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA) #higher accuracy target use, slower
            #net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16) #reduced latency nn processing, slight hit on accuracy
        else:
            net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV) #will target standard opencv build on Darwin and Windows 
            net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU) #CPU target, no GPU use. Slower, but for testing system

        self.model = cv2.dnn_DetectionModel(net)
        self.model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

    def detection(self, frame):
        classes, scores, boxes = self.model.detect(frame, self.confidence, self.nmsThreshold)

        return classes, scores, boxes


class outputTesting:
    def __init__(self, names_file):
        self.color = (0, 255, 255)
        self.class_names = []
        with open(names_file, 'r') as f:
            self.class_names = [cname.strip() for cname in f.readlines()]

    def testOutputFrames(self, frame, tracked_fish): 
        for t in tracked_fish:
            label = "%s" % (self.class_names[t[1]] + ", id: " + str(t[0]) + ", max_score: " + str(t[2]))
            cv2.rectangle(frame, t[3], self.color, 2)
            cv2.putText(frame, label, (t[3][0], t[3][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 2.5,
                        self.color, 6)
        #frame = cv2.resize(frame, (360,640)) #good for lotic.demo vid since its 4k
        #cv2.imshow("detections", frame) #For visualizing live detections, uncomment this line
