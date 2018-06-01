## Requirements
* Python 2.7
* Linux packages: python-dev and python-pip
* Python packages: setuptools, tox and flake8

To **apt** distros, you can use [pre-install.sh](https://github.com/bigsea-ufcg/bigsea-monitor/tree/master/tools/pre-install.sh) to install the requirements.

## Install
Clone the [Monitor repository](https://github.com/bigsea-ufcg/bigsea-monitor.git) in your machine.

### Configuration
A configuration file is required to run the Monitor. **Edit and fill your monitor.cfg in the root of Monitor directory.** Make sure you have fill up all fields before run.
You can find a template in [config-example.md](https://github.com/bigsea-ufcg/bigsea-monitor/tree/master/docs/config-example.md). 

### Run
In the Monitor root directory, start the service using run script:
```
$ ./run.sh
```

Or using tox command:
```
$ tox -e venv -- monitor
```
