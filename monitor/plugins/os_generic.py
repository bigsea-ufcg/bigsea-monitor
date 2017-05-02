import paramiko
import time

from monitor.monasca.manager import MonascaMonitor
from monitor.plugins.base import Plugin


class OSGeneric(Plugin):

    def __init__(self, app_id, info_plugin, collect_period, keypair, retries=60):
        Plugin.__init__(self, collect_period, retries=retries)
        self.app_id = app_id
        self.host_ip = info_plugin['host_ip']
        self.expected_time = info_plugin['expected_time']
        self.keypair_path = keypair
        self.host_username = 'ubuntu'
        self.log_path = info_plugin['log_path']
        self.dimensions = {"application_id": self.app_id,
                           "host": self.host_ip}
        self.last_checked = ''
        self.start_time = time.time()
        self.monasca = MonascaMonitor()


    def _get_metric_value(self, log):
        value = None
        for i in range(len(log) - 1, 0, -1):
            if log[i] == '#':
                value = float(log[i + 1:-1])
        return value

    def _get_elapsed_time(self):
        delay = time.time() - self.start_time
        return delay

    def _get_ssh_connection(self):
        keypair = paramiko.RSAKey.from_private_key_file(self.keypair_path)
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(hostname=self.host_ip, username=self.host_username, pkey=keypair)
        return conn

    def _publish_metrics(self, last_log):
        metric = {}
        print last_log
        # Check if this log line contains a new metric measurement
        if '[Progress]' in last_log and self.last_checked != last_log:
            self.last_checked = last_log
            # Add to metric_info values for this measurement:
            # value and timestamp
            ref_value = self._get_elapsed_time() / self.expected_time
            measurement_value = self._get_metric_value(last_log)
            error = measurement_value - ref_value
            metric['name'] = 'application-progress.error'
            metric['value'] = error
            metric['timestamp'] = time.time() * 1000
            metric['dimensions'] = self.dimensions
            # Sending the metric to Monasca
            self.monasca.send_metrics([metric])
            print "Application progress error: %.4f" % error

        # Flag that checks if the log capture is ended
        elif '[END]' in last_log:
            self.running = False

    def monitoring_application(self, dimensions, app_id):
        try:

            conn = self._get_ssh_connection()
            stdin , stdout, stderr = conn.exec_command("sudo tail -1 %s" % self.log_path)
            self._publish_metrics(stdout.read())

        except Exception as ex:
            print "Monitoring %s is not possible. \nError: %s. %s remaining attempts" % (self.app_id, ex.message,
                                                                                         self.attempts)
            raise ex
