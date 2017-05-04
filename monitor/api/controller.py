# Copyright (c) 2017 UFCG-LSD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ConfigParser
import os
import sys

from monitor import api
from monitor.plugins.spark_progress import SparkProgress
from monitor.plugins.web_log_monitor import WebAppMonitor
from monitor.plugins.os_generic import OSGeneric


class Controller:

    def __init__(self):
        # This dictionary contains all the plugins objects where the key is the application_id and
        # the value is the own plugin object.
        self.app_monitored = {}
        self.retries = api.retries
        self.os_keypair = api.os_keypair

    def start_monitor(self, plugin_name, app_id, info_plugin, collect_period):
        print "Starting monitoring..."
        plugin = None

        # These conditional cases choose the class plugin's constructor of the application submitted
        # Note: some plugins need the keypair to access remotely some machine and execute the monitoring
        # logic, but this attribute is not mandatory for all the plugins.
        if app_id not in self.app_monitored:
            if plugin_name == "spark_progress":
                plugin = SparkProgress(app_id, info_plugin, collect_period, retries=60)
                self.app_monitored[app_id] = plugin
            elif plugin_name == "web_app_monitor":
                plugin = WebAppMonitor(app_id, info_plugin, collect_period, self.os_keypair, retries=60)
                self.app_monitored[app_id] = plugin
            elif plugin_name == "os_generic":
                plugin = OSGeneric(app_id, info_plugin, collect_period, self.os_keypair, retries=60)
                self.app_monitored[app_id] = plugin

            print "Starting plugin: %s" % plugin.getName()
            plugin.start()

        else:
            print "The application is already being monitored"

    def kill_monitor(self, app_id):
        try:
            # Stop the plugin and remove from the data structure
            self.app_monitored.pop(app_id, None).stop()
        except Exception as ex:
            ex.message
            pass

