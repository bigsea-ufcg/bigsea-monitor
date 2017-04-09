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

    def __init__(self, app_id, info_plugin, collect_period):
        Plugin.__init__(self, collect_period)
        self.submission_url = info_plugin['spark_submisson_url']
        self.app_id = app_id
        self.expected_time = info_plugin['expected_time']
        self.monasca = MonascaMonitor()
        self.dimensions = {'application_id': self.app_id, 'service': 'spark-sahara'}

    def get_elapsed_time(self, gmt_timestamp):
        local_tz = tzlocal.get_localzone()
        date_time = datetime.strptime(gmt_timestamp, '%Y-%m-%dT%H:%M:%S.%fGMT')
        date_time = date_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
        elapsed_time = datetime.now() - date_time.replace(tzinfo=None)
        return elapsed_time.seconds

    def _publish_measurement(self, job_request, dimensions):

        job_progress = {}
        time_progress = {}

        for result in job_request.json():

            timestamp = time.time() * 1000
            progress = result['numCompletedTasks'] / float(result['numTasks'])
            progress = float("{:10.4f}".format(progress))
            used_time = self.get_elapsed_time(result['submissionTime']) / float(self.expected_time)
            # self.logger.log("%s,%s" % (progress, used_time))
            job_progress['name'] = 'spark.job_progress'
            job_progress['value'] = progress
            job_progress['timestamp'] = timestamp
            job_progress['dimensions'] = dimensions
            time_progress['name'] = 'spark.elapsed_time'
            time_progress['value'] = used_time
            time_progress['timestamp'] = timestamp
            time_progress['dimensions'] = dimensions
            self.monasca.send_metrics([job_progress, time_progress])

            time.sleep(MONITORING_INTERVAL)

    def monitoring_application(self, dimensions, app_id):
        print "toaqui"

        try:

            job_request = requests.get(self.submission_url + ':4040/api/v1/applications/' + app_id + '/jobs')

            self._publish_measurement(job_request, dimensions)

        except Exception as ex:
            self.attempts -= 1
            print "Error: No application found for %s\n%s remaining attempts" % (self.app_id, self.attempts)
            raise
