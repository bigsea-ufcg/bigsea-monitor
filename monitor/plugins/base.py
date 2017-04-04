import threading
import time


class Plugin(threading.Thread):

    def __init__(self, collect_period):
        threading.Thread.__init__(self)
        self.running = False
        self.dimensions = {}
        self.collect_period = collect_period
        self.attempts = 120
        self.app_id = None

    def stop(self):
        print "The %s is stopping for %s..." % (type(self).__name__, self.app_id)
        self.running = False

    def monitoring_application(self, dimensions, app_id):
        pass

    def run(self):

        self.running = True
        while self.running:
            if self.attempts == 0:
                self.stop()
                break
            try:
                time.sleep(self.collect_period)
                self.monitoring_application(self.dimensions, self.app_id)
                self.attempts = 5

            except Exception as ex:
                # print ex.message
                pass
