import threading


class Plugin(threading.Thread):

    def __init__(self):
        threading.Thread.__init__()
        self.running = False

    def stop(self):
        self.running = False
