import ConfigParser
import os
import sys

from monitor.plugins.spark_progress import SparkProgress
from monitor.plugins.web_log_monitor import WebAppMonitor

config = ConfigParser.RawConfigParser()
__file__ = os.path.join(sys.path[0], '../../monitor.cfg')
config.read(__file__)


class Controller:

    def __init__(self):
        self.app_monitored = {}
        self.retries = config.getint('service', 'retries')
        self.os_user = config.get('openstack', 'user')
        self.os_password = config.get('openstack', 'password')
        self.os_project_id = config.get('openstack', 'project_id')
        self.os_user_domain = config.get('openstack', 'user_domain')
        self.os_keypair = config.get('openstack', 'key_pair')

    def start_monitor(self, plugin_name, app_id, info_plugin, collect_period):
        print "Starting monitoring..."
        plugin = None

        if app_id not in self.app_monitored:
            if plugin_name == "spark_progress":
                plugin = SparkProgress(app_id, info_plugin, collect_period, retries=60)
                self.app_monitored[app_id] = plugin
            elif plugin_name == "web_app_monitor":
                plugin = WebAppMonitor(app_id,
                                       info_plugin,
                                       collect_period,
                                       self.os_keypair,
                                       retries=60)
                self.app_monitored[app_id] = plugin
            print "Starting plugin: %s" % plugin.getName()
            plugin.start()

        else:
            print "The application is already being monitored"

    def kill_monitor(self, app_id):
        try:
            self.app_monitored.pop(app_id, None).stop()
        except Exception as ex:
            ex.message
            pass

