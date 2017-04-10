import ConfigParser
import os
import sys

from monitor.plugins.spark_progress import SparkProgress

config = ConfigParser.RawConfigParser()
__file__ = os.path.join(sys.path[0], '../../monitor.cfg')
config.read(__file__)


class Controller:

    def __init__(self):
        self.app_monitored = {}
        self.retries = config.getint('service', 'retries')

    def start_monitor(self, plugin_name, app_id, info_plugin, collect_period):
        print "Starting monitoring..."
        plugin = None

        if app_id not in self.app_monitored:
            if plugin_name == "spark_progress":
                plugin = SparkProgress(app_id, info_plugin, collect_period, retries=60)
                self.app_monitored[app_id] = plugin

            print "Starting plugin: %s" % plugin.getName()
            plugin.start()

        else:
            print "The application  is already being monitored"

    def kill_monitor(self, app_id):
        try:
            self.app_monitored.pop(app_id, None).stop()
        except Exception as ex:
            ex.message
            pass

