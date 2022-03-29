import threading

class LoticSignal:
    def __init__(self):
        self.__lock = threading.Lock()
        self.__keep_running = True

    def handler(self, num, frame):
        with self.__lock:
            self.__keep_running = False

    def keep_running(self):
        with self.__lock:
            return self.__keep_running
