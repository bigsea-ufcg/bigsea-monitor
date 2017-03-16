import requests
import time
import tzlocal
import pytz
import monitor

from datetime import datetime
from server.utils.logger import *



LOG_FILE = "progress.log"
TIME_PROGRESS_FILE = "time_progress.log"
MONITORING_INTERVAL = 2

class SparkMonitoring():

    def __init__(self, spark_submisson_url, expected_time):
        self.submission_url = spark_submisson_url
        self.monasca = monitor.MonascaMonitor()
        self.expected_time = expected_time
        # self.logger = Log("ServerLog2", "server.log")
        # configure_logging()


    def get_running_app(self):
        try:
            all_app = requests.get(self.submission_url +
                                   ':8080/api/v1/applications?status=running')
            for app in all_app.json():
                if app['attempts'][0]['completed'] == False:
                    return app['id'], app['name']
            return None
        except:
            # self.logger.log("No application found")
            return None

    def get_elapsed_time(self, gmt_timestamp):
        local_tz = tzlocal.get_localzone()
        date_time = datetime.strptime(gmt_timestamp, '%Y-%m-%dT%H:%M:%S.%fGMT')
        date_time = date_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
        elapsed_time = datetime.now() - date_time.replace(tzinfo=None)
        return elapsed_time.seconds

    def get_single_job(self):
        app = None
        for i in range(0, 50):
            #self.logger.log('Attempt %s' % i)
            application = self.get_running_app()
            if application is not None:
                app = application
                break
            time.sleep(5)

        return app

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

    def _monitoring_application(self, dimensions, app_id):
        try:
            job_request = requests.get(self.submission_url + ':4040/api/v1/applications/' + app_id + '/jobs')

            self._publish_measurement(job_request, dimensions)

        except Exception as ex:
            # self.logger.log("SparkMonitoring Error: %s" % ex.message)
            try:
                job_request = requests.get(self.submission_url + ':8080/api/v1/applications/' + app_id)

                if job_request.json()['attempts'][0]['completed']:
                    timestamp = time.time() * 1000
                    job_progress = {}

                    job_progress['name'] = 'spark.job_progress'
                    job_progress['value'] = 1
                    job_progress['timestamp'] = timestamp
                    job_progress['dimensions'] = dimensions

                    self.monasca.send_metrics([job_progress])

                    # self.logger.log("Application %s completed." % app_id)
                    # self.logger.log("%s | Finishing Monitor" % (time.strftime("%H:%M:%S")))
                else:
                    pass
                    # self.logger.log("SparkMonitoring Error1: %s" % ex.message)
            except Exception as ex:
                # self.logger.log("SparkMonitoring Error2: %s" % ex.message)
                pass

    def run(self):

        app = self.get_single_job()

        # self.logger.log("%s | Spark application id: %s" % (time.strftime("%H:%M:%S"),app[0]))
        # self.logger.log("%s | Starting Monitor" % (time.strftime("%H:%M:%S")))

        if app is not None:
            app_id = app[0]
            dimensions = {'application_id': app_id, 'service': 'spark-sahara'}

            while True:
                try:
                    self._monitoring_application(dimensions, app_id)
                except Exception as ex:
                    print ex.message
                    break
