# Copyright (c) 2018 UFCG-LSD.
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


class KubeJobProgress(Plugin):
    def __init__(self, app_id, info_plugin, collect_period=2, retries=60):
        Plugin.__init__(self, app_id, info_plugin,
                        collect_period, retries=retries)

        self.monasca = MonascaMonitor()

        self.submission_url = info_plugin['count_jobs_url']
        self.expected_time = int(info_plugin['expected_time'])
        self.number_of_jobs = int(info_plugin['number_of_jobs'])
        self.submission_time = datetime.strptime(info_plugin['submission_time'],
                                                 '%Y-%m-%dT%H:%M:%S.%fGMT')
        self.dimensions = {'application_id': self.app_id,
                           'service': 'kubejobs'}

        self.current_job_id = 0

    def _publish_measurement(self, job_request):


        application_progress_error = {}
        job_progress_error = {}
        time_progress_error = {}

        # Init
        jobs_completed = int(job_request.json())
        print "Completed: %i" % jobs_completed

        # Job Progress

        job_progress = (float(jobs_completed) / self.number_of_jobs)

        # Elapsed Time
        elapsed_time = float(self._get_elapsed_time())

        # Reference Value
        ref_value = (elapsed_time / self.expected_time)

        # Error
        print "\nJob progress: %s\nRef_value: %s\n" % (job_progress, ref_value)
        error = job_progress - ref_value

        application_progress_error['name'] = ('application-progress'
                                              '.error')

        job_progress_error['name'] = ('job-progress'
                                              '.error')

        time_progress_error['name'] = ('time-progress'
                                              '.error')

        application_progress_error['value'] = error
        application_progress_error['timestamp'] = time.time() * 1000
        application_progress_error['dimensions'] = self.dimensions

        job_progress_error['value'] = job_progress
        job_progress_error['timestamp'] = time.time() * 1000
        job_progress_error['dimensions'] = self.dimensions

        time_progress_error['value'] = ref_value
        time_progress_error['timestamp'] = time.time() * 1000
        time_progress_error['dimensions'] = self.dimensions

        print application_progress_error['value']

        self.monasca.send_metrics([application_progress_error])
        self.monasca.send_metrics([job_progress_error])
        self.monasca.send_metrics([time_progress_error])


        time.sleep(MONITORING_INTERVAL)

    def _get_elapsed_time(self):
        try:
            local_tz = tzlocal.get_localzone()
            print local_tz

        except Exception as e:
            print e.message
            local_tz = "America/Recife"
            local_tz = pytz.timezone(local_tz)

        print "Submission time: %s" % self.submission_time
        # init_time = self.submission_time
        # init_time = init_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
        # init_time = init_time.replace(tzinfo=None)
        datetime_now = datetime.now()
        print "Time now: %s" % str(datetime_now)
        elapsed_time = datetime_now - self.submission_time
        print "Elapsed Time: %.2f" % elapsed_time.seconds

        return elapsed_time.seconds

    def monitoring_application(self):
        try:
            job_request = requests.get(self.submission_url +
                                       '/%s:results/count' % self.app_id)

            self._publish_measurement(job_request)

        except Exception as ex:
            print ("Error: No application found for %s. %s remaining attempts"
                   % (self.app_id, self.attempts))

            print ex.message
            raise
