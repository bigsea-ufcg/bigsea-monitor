# BIGSEA Asperathos - Monitor

## Overview
The Monitor component is responsible for capturing, calculating and publishing applications metrics that will be used by the controller or load balance services.

To more info, see [details.md](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/details.md)

## How does it works?
The monitor is implemented following a **plugin architecture**, allowing the framework to monitor different types of application and different metrics of interest related to the QoS of the applications.

## How to develop a plugin?
See [plugin-development.md](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/plugin-development.md).

## Requirements
* Python 2.7 or Python 3.5
* Linux packages: python-dev and python-pip
* Python packages: setuptools, tox and flake8

To **apt** distros, you can use [pre-install.sh](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/tools/pre-install.sh) to install the requirements.

## Install
First of all, install **git**. After, you just need to clone the [Monitor repository](https://github.com/bigsea-ufcg/bigsea-monitor.git) in your machine.

### Configuration
A configuration file is required to run the Monitor. **Edit and fill your monitor.cfg in the root of Monitor directory.** Make sure you have fill up all fields before run.
You can find a template in [config-example.md](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/config-example.md). 

### Run
In the Monitor root directory, start the service using tox command:
```
$ tox -e venv -- monitor
```

## Monitor REST API
Endpoints is avaliable on [restapi-endpoints.md](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/restapi-endpoints.md) documentation.

## Avaliable plugins
* [Spark Sahara](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/plugins/spark_sahara.md)
* [Spark Mesos](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/plugins/spark_mesos.md)
* [Openstack Generic](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/plugins/openstack_generic.md)
* [Web Application](https://github.com/bigsea-ufcg/bigsea-monitor/tree/refactor/docs/plugins/web_app.md)
