from flask import request
from monitor.api.controller import Controller

import monitor.utils.api as api_util

rest_api = api_util.Rest('v1', __name__)
monitor = Controller()

START = '/start'
STOP = '/stop/<app_id>'


@rest_api.post('/start')
def start(data):
    data = request.json
    print data
    plugin = data['plugin']
    info_plugin = data['info_plugin'] or None
    collect_period = data['collect_period']
    monitor.start_monitor(plugin, info_plugin, collect_period)

    return "ok"


@rest_api.post(STOP)
def stop(data, app_id):
    monitor.kill_monitor(app_id)

    return "ok"
