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

config = ConfigParser.RawConfigParser()
config.read('./monitor.cfg')

monasca_endpoint = config.get('monasca', 'monasca_endpoint')
monasca_username = config.get('monasca', 'username')
monasca_password = config.get('monasca', 'password')
monasca_auth_url = config.get('monasca', 'auth_url')
monasca_project_name = config.get('monasca', 'project_name')
monasca_api_version = config.get('monasca', 'api_version')

retries = config.getint('service', 'retries')
host_address = config.get('service', 'host')
host_port = config.getint('service', 'port')
use_debug = config.get('service', 'debug')

os_keypair = config.get('credentials', 'key_pair')
mesos_cluster_addr = config.get('credentials', 'mesos_cluster_addr')
mesos_password = config.get('credentials', 'mesos_password')
mesos_username = config.get('credentials', 'mesos_username')
