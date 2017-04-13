# BigSea Monasca Monitor

#### How to run


* Configure the monitor.cfg providing the following info:
```
[monasca]
username = <monasca_username>
password = <password>
project_name = <monasca_project>
auth_url = http://<monasca_end_point>:<keystone_port>/v3/
api_version = 2_0

[service]
host = <host_ip>
port = <host_port>
debug = True
```
* Run the main python file to lift the service
```
$ python monitor/cli/main.py
```

#### How to start monitoring

POST /start/<app_id>
Request body:
```javascript
{
	"plugin": "<plugin_name>",
	"info_plugin":{<info_keys>: <info_values>},
	"collect_period": <interval_in_seconds>
}
```

#### How to stop monitoring

POST /stop/<app_id>

#### Plugins Examples

##### SparkProgress

POST /start/app-20170411192759-0026
Request body:
```javascript
{
	"plugin": "spark_progress",
	"info_plugin":{
	                "spark_submisson_url":"http://10.11.4.11",
					"expected_time": 500

	},
	"collect_period": 2
}
```

##### Web-App

POST /start/web-app-01
Request body:
```javascript
{
	"plugin": "web_app_monitor",
	"info_plugin": {"host_ip":"10.57.4.1",
					"host_username": "ubuntu",
					"log_path":"/var/log/web-app.log"
	},
	"collect_period": 1
}
```
