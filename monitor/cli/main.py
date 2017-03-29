from monitor.cli import *

import ConfigParser
import os

config = ConfigParser.RawConfigParser()
__file__ = os.path.realpath("../../monitor.cfg")
config.read(__file__)

host_address = config.get('service', 'host')
host_port = int(config.get('service', 'port'))
use_debug = config.get('service', 'debug')

main(host_address, host_port, use_debug)
