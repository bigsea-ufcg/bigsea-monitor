import json
import threading
from core.main import Controller
from flask import Flask
from flask import request
import ConfigParser

app = Flask(__name__)

config = ConfigParser.RawConfigParser()
config.read('./monitor.cfg')

controller = Controller()


@app.route('/', methods=['POST'])
def start():
    data = request.json
    plugin = data['plugin']
    info_plugin = data['info_plugin']
    controller.start_monitor(plugin, info_plugin)
    # spark_url = data['spark_id']
    # spark_id = data['spark_id']
    # start_time = data['start_time']
    # collect_period = data['collect_period'] or None


@app.route('/stop/<app_id>', methods=['GET'])
def stop(app_id):
    controller.kill_monitor(app_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=666, debug=True)