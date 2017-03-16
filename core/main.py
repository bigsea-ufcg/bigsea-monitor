import threading

from monasca.manager import MonascaMonitor
from plugins.spark_progress import SparkMonitoring

class Controller:

    def __init__(self):
        self.monasca = MonascaMonitor
        self.app_monitored = []

    def start_monitor(self, plugin_name, info_plugin):

        if plugin_name == "spark_progress":
            plugin = SparkMonitoring()
            self.app_monitored.append(info_plugin['spark_id'])

        monitor = threading.Thread(target=plugin.run(), kwargs=info_plugin)
        monitor.run()
        pass

    def kill_monitor(self, spark_id):
        pass

    def run(self, spark_id, spark_url, start_time, collect_period=2):
        pass