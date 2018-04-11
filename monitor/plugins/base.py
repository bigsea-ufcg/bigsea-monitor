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

import threading
import time
from monitor.monasca.manager import MonascaMonitor


# Plugins must extend Thread to facilitate each parallel plugin execution
class Plugin(threading.Thread):

    def __init__(self, app_id, info_plugin, collect_period, retries=30):
        threading.Thread.__init__(self)
        # Contains all the specific information for each plugin
        self.info_plugin = info_plugin
        # Flag that enable or disable the monitoring logic execution
        self.running = False
        # Dimensions is composed by default only application_id, but for each plugin
        # it can change and it is possible to add some relevant information
        self.dimensions = {'application_id': app_id}
        # Time interval between each metric collect
        self.collect_period = collect_period
        # How many times monitoring_application must be re executed when something break into the execution
        self.attempts = retries
        # The identifier for the submitted application
        self.app_id = app_id

    def stop(self):
        print "The %s is stopping for %s..." % (type(self).__name__, self.app_id)
        self.running = False

        monasca = MonascaMonitor()
        app_progress_metric = {}
        app_progress_metric['name'] = ('application-progress.app_progress')
        app_progress_metric['value'] = 100
        app_progress_metric['timestamp'] = time.time() * 1000
        dimensions = {'application_id': self.app_id,
                      'service': 'spark-sahara'}
        app_progress_metric['dimensions'] = dimensions
        monasca.send_metrics([app_progress_metric])

    # This method must be subscribed by each plugin that extends this base class
    def monitoring_application(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            if self.attempts == 0:
                self.stop()
                break
            try:
                time.sleep(self.collect_period)
                self.monitoring_application()

            except Exception as ex:
                self.attempts -= 1
                print ex.message
                pass
