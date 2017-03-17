import threading


class Plugin(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False
        self.dimensions = {}

    def stop(self):
        self.running = False

    def monitoring_application(self, dimensions, app_id):
        pass

    def run(self):
        self.running = True
        while self.running:
            try:
                self.monitoring_application(self.dimensions, self.app_id)
            except Exception as ex:
                print ex.message
                break