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

from monascaclient import client as monclient, ksclient
import monascaclient.exc as exc
import socket
import time

LOG_PATH = "./batch.log"
last_checked = ''

# A metric identity is composed by its name and dimensions (a dictionary
# that represents attributes, as the host of the metric owner and the
# application id). For this example, socket.getfqdn() gets the context hostname.
metric_info = {'name': 'metric.name',
               'dimensions': {
                   'hostname': socket.getfqdn()
                              }
               }

# Monasca client needs authenticate via keystone. Creating a keystone
# client is possible to get a token that will be used after to create a
# Monasca client.
ks = ksclient.KSClient(
            auth_url='http://<keystone_url>:5000/v3',
            username='user',
            password='password',
            project_name='monasca'
        )

# Creating a monasca client using the keystone token
monasca_client = monclient.Client(
            '2_0', ks.monasca_url, token=ks.token
        )


# For this approach, the format of the log must follow some pattern.
# The method get_metric_value extract the value from this log pattern.
# Flags are used to capture logs of interest and value into these logs
# For this use case "#" is a token to identify where exactly the value
# is located and makes possible to convert the string to float value.
def get_metric_value(log):
	for i in range(len(log)-1, 0, -1):
		if log[i] == '#':
			value = float(log[i+1:len(log)])

	return value

# This loop checks new logs continously and publish a new measurement into
# Monasca when it is identified.
while True:
    log = open(LOG_PATH, "r")
    latest_log = log.readlines()
	# Check if log file is still empty
    if latest_log != []:
        latest_log = latest_log[-1]

        # Check if this log line contains a new metric measurement
        if '[Random]' in latest_log and last_checked != latest_log:
                last_checked = latest_log
                # Add to metric_info values for this measurement:
                # value and timestamp
                value = get_metric_value(latest_log)
                metric_info['name'] = 'batch.random'
                metric_info['value'] = value
                metric_info['timestamp'] = time.time() * 1000
                # Sending the metric to Monasca
                monasca_client.metrics.create(**metric_info)
                print "Progress published: %.2f" % (value)

        elif '[Elapsed Time]' in latest_log and last_checked != latest_log:
                last_checked = latest_log
                # Add to metric_info values for this measurement:
                # value and timestamp
                value = get_metric_value(latest_log)
                metric_info['name'] = 'elapsed_time'
                metric_info['value'] = value
                metric_info['timestamp'] = time.time() * 1000
                # Sending the metric to Monasca
                monasca_client.metrics.create(**metric_info)
                print "Elapsed Time published: %.2f" % (value)

        # Flag that checks if the log capture is ended
        elif '[END]' in latest_log:
                break
