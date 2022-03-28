import cv2
import queue

class frameImport:
    def __init__(self, video_input, lotic_signal):
        self.video_input = video_input
        self.frame_input_queue = queue.Queue(100)
        self.lotic_signal = lotic_signal

    def videoSource(self):
        self.video_source = cv2.VideoCapture(self.video_input)
        return self.video_source

    def receiveFrame(self):
        while self.lotic_signal.keep_running():
            grabbed, self.frame = self.video_source.read()
            if not grabbed:
                # Todo: you probably don't wanna do this in the "it runs forever"
                # case. This is only useful for reading video files with an end.
                # But I think that's what you want here, so...
                print("not grabbed")
                break
            self.frame_input_queue.put(self.frame)

    def grabFrame(self):
        try:
            return self.frame_input_queue.get(timeout=3)
        except queue.Empty:
            return None
