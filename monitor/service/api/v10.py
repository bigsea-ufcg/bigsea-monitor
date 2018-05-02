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

from monitor.service import api
from monitor import exceptions as ex
from monitor.utils.logger import Log
from monitor.plugins.spark_sahara.plugin import SparkProgress
from monitor.plugins.spark_mesos.plugin import SparkProgressUPV
from monitor.plugins.web_log_monitor.plugin import WebAppMonitor
from monitor.plugins.openstack_generic.plugin import OSGeneric


API_LOG = Log("APIv10", "APIv10.log")

monitored_apps = {}


def start_monitoring(data, app_id):
    """ These conditional cases choose the class executor's constructor of the 
    application submitted
    Note: some executors need the keypair to access remotely some machine and
    execute the monitoring logic, but this attribute is not mandatory for all
    the executors."""

    if 'plugin' not in data.keys() or 'plugin_info' not in data.keys():
        API_LOG.log("Missing parameters in request")
        raise ex.BadRequestException()

    plugin = data['plugin']
    plugin_info = data['plugin_info']
    
    executor = None
    if app_id not in monitored_apps:
        if plugin == "spark_sahara":
            import pdb; pdb.set_trace()
            executor = SparkProgress(app_id, plugin_info, api.retries)
            monitored_apps[app_id] = executor

        elif plugin == "web_app_monitor":
            executor = WebAppMonitor(app_id, plugin_info, api.os_keypair,
                                     api.retries)
            monitored_apps[app_id] = executor

        elif plugin == "openstack_generic":
            executor = OSGeneric(app_id, plugin_info, api.os_keypair,
                                 api.retries)
            monitored_apps[app_id] = executor

        elif plugin == "spark_mesos":
            executor = SparkProgressUPV(app_id, plugin_info, api.retries)
            monitored_apps[app_id] = executor
       
        else:
            API_LOG.log("Plugin does not exists")
            raise ex.BadRequestException()

        API_LOG.log("Starting monitoring: %s" % executor.getName())
        executor.start()

    else:
        API_LOG.log("The application is already being monitored")
        raise ex.BadRequestException()


def stop_monitoring(app_id):
    try:
        # Stop the plugin and remove from the data structure
        monitored_apps.pop(app_id, None).stop()
    except Exception as ex:
        ex.message
        pass
