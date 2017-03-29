import threading
import time


class Plugin(threading.Thread):

    def __init__(self, collect_period):
        threading.Thread.__init__(self)
        self.running = False
        self.dimensions = {}
        self.collect_period = collect_period

    def stop(self):
        self.running = False

    def monitoring_application(self, dimensions, app_id):
        pass

    def run(self):

        self.running = True
        while self.running:
            try:
                self.monitoring_application(self.dimensions, self.app_id)
                time.sleep(self.collect_period)

            except Exception as ex:
                print ex.message
