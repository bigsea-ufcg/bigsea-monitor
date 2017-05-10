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

import time
from datetime import datetime

import pytz
import requests
import tzlocal
from monitor.monasca.manager import MonascaMonitor
from monitor.plugins.base import Plugin

LOG_FILE = "progress.log"
TIME_PROGRESS_FILE = "time_progress.log"
MONITORING_INTERVAL = 2


class SparkProgress(Plugin):

    def __init__(self, app_id, info_plugin, collect_period, retries=60):
        Plugin.__init__(self, app_id, info_plugin, collect_period, retries=retries)
        self.submission_url = info_plugin['spark_submisson_url']
        self.expected_time = info_plugin['expected_time']
        self.monasca = MonascaMonitor()
        self.dimensions = {'application_id': self.app_id, 'service': 'spark-sahara'}

    def _get_elapsed_time(self, gmt_timestamp):
        try:
            local_tz = tzlocal.get_localzone()
        except Exception as e:
            local_tz = "America/Recife"
            local_tz = pytz.timezone(local_tz)
        date_time = datetime.strptime(gmt_timestamp, '%Y-%m-%dT%H:%M:%S.%fGMT')
        date_time = date_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
        elapsed_time = datetime.now() - date_time.replace(tzinfo=None)
        return elapsed_time.seconds

    def _publish_measurement(self, job_request):

        application_progress_error = {}

        for result in job_request.json():

            progress = result['numCompletedTasks'] / float(result['numTasks'])
            progress = float("{:10.4f}".format(progress))
            # Add to metric_info values for this measurement:
            # value and timestamp
            ref_value = self._get_elapsed_time(result['submissionTime']) / float(self.expected_time)
            error = progress - ref_value
            # The Monasca metric must have the 3 following fields to be created: name, value and timestamp,
            # but also is possible to increment the metrics identities - using dimensions -  and informations -
            # using value_meta, a dictionary that contains aditional information about the measurement  .
            application_progress_error['name'] = 'application-progress.error'
            application_progress_error['value'] = error
            application_progress_error['timestamp'] = time.time() * 1000
            application_progress_error['dimensions'] = self.dimensions
            # Sending the metric to Monasca
            self.monasca.send_metrics([application_progress_error])


            print "Metric successfully published"

            time.sleep(MONITORING_INTERVAL)

    def monitoring_application(self):
        try:
            
            job_request = requests.get(self.submission_url + ':4040/api/v1/applications/' + self.app_id + '/jobs')
            
            self._publish_measurement(job_request)

        except Exception as ex:
            print "Error: No application found for %s. %s remaining attempts" % (self.app_id, self.attempts)
            print ex.message
            raise
