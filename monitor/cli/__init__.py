from flask import Flask
from monitor.api.v1 import rest_api


def main(host, port, debug):
    app = Flask(__name__)
    app.register_blueprint(rest_api)
    app.run(host=host, port=port, debug=debug)