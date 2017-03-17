from core.monitor import Monitor
from flask import Flask
from flask import request

app = Flask(__name__)
monitor = Monitor()


@app.route('/', methods=['POST'])
def start():
    data = request.json
    plugin = data['plugin']
    info_plugin = data['info_plugin'] or None
    monitor.start_monitor(plugin, info_plugin)


@app.route('/stop/<app_id>', methods=['GET'])
def stop(app_id):
    monitor.kill_monitor(app_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=666, debug=True)