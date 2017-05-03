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


class Plugin(threading.Thread):

    def __init__(self, app_id, info_plugin, collect_period, retries=30):
        threading.Thread.__init__(self)
        self.info_plugin = info_plugin
        self.running = False
        self.dimensions = {'application_id': app_id}
        self.collect_period = collect_period
        self.attempts = retries
        self.app_id = app_id

    def stop(self):
        print "The %s is stopping for %s..." % (type(self).__name__, self.app_id)
        self.running = False

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
