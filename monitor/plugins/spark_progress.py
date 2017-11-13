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
        Plugin.__init__(self, app_id, info_plugin,
                        collect_period, retries=retries)

        self.monasca = MonascaMonitor()

        self.submission_url = info_plugin['spark_submisson_url']
        self.expected_time = info_plugin['expected_time']

        self.remaining_time = int(self.expected_time)
        self.job_expected_time = int(self.expected_time)

        self.number_of_jobs = int(info_plugin['number_of_jobs'])
        self.current_job_id = 0

        self.dimensions = {'application_id': self.app_id,
                           'service': 'spark-sahara'}


    def _publish_measurement(self, job_request):

        application_progress_error = {}

        # Init
        jobs = job_request.json()
        jobs.reverse()

        if not len(jobs) == 0:
            current_job = jobs[self.current_job_id]
            
            if current_job['status'] == 'FAILED':
                self.current_job_id = len(jobs) - 1

            elif current_job['status'] == 'SUCCEEDED':
                elapsed_time = float(self._get_elapsed_time(
                               current_job['submissionTime']))            

                self.remaining_time = self.remaining_time - elapsed_time

                self.current_job_id = len(jobs) - 1

                # Job Time
                self.job_expected_time = (self.remaining_time
                                 / (float(self.number_of_jobs)
                                 - float(self.current_job_id)))

            elif current_job['status'] == 'RUNNING':
                # Job Progress
                job_progress = (current_job['numCompletedTasks']
                                / float(current_job['numTasks']))

                # Elapsed Time
                elapsed_time = float(self._get_elapsed_time(
                               current_job['submissionTime']))
                
                # Reference Value
                ref_value = (elapsed_time / self.job_expected_time)
                
                # Error
                error = job_progress - ref_value
                
                application_progress_error['name'] = 'application-progress.\
                                                      error'

                application_progress_error['value'] = error
                application_progress_error['timestamp'] = time.time() * 1000
                application_progress_error['dimensions'] = self.dimensions

                print application_progress_error['value']
                
                self.monasca.send_metrics([application_progress_error])
                
            time.sleep(MONITORING_INTERVAL)


    def _get_elapsed_time(self, gmt_timestamp):
        try:
            local_tz = tzlocal.get_localzone()

        except Exception as e:
            local_tz = "America/Recife"
            local_tz = pytz.timezone(local_tz)

        date_time = datetime.strptime(gmt_timestamp, '%Y-%m-%dT%H:%M:%S.%fGMT')
        date_time = date_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
        date_time = date_time.replace(tzinfo=None)
        datetime_now = datetime.now()
        elapsed_time = datetime_now - date_time

        return elapsed_time.seconds


    def monitoring_application(self):
        try:

            job_request = requests.get(self.submission_url
                          + ':4040/api/v1/applications/'
                          + self.app_id + '/jobs')

            self._publish_measurement(job_request)

        except Exception as ex:
            # FIXME: @armstrongmsg - self.attempts is not updated anywhere. 
            #        I think you should remove it from this message.
            print ("Error: No application found for %s. %s remaining attempts"
                   % (self.app_id, self.attempts))

            print ex.message
            raise
