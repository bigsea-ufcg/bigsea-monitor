# Plugin development
This is an important step to enjoy all flexibility and features that this framework provides.

## Steps
1. Write a new python class into the path: *monitor/plugins*. This class must extend *monitor.plugins.base* and implement only two methods: __init__ and  monitoring_application.

* **__init__(self, app_id, plugin_info, collect_period, retries=60)**
	* **app_id**: it is the application id. It is the only mandatory information about the metric identity, although there may be others.
	* **collect_period**: the time interval to execute monitoring_application.
	* **retries**: the number of retries when some problem any problem occurs during the any of the steps to gather metrics and publish into the metric store service. When all the retries are consumed, the monitoring service for this application will stop. If the problem disappears before the end of the retries, the retries number reload the initial value. (e.g. the connection is failing with the host where I’m accessing remotely but I don’t wanna give up to monitor this host because this problem can be for a little lapse of time).
	* **plugin_info**: it is a dictionary that contains all the information needed specifically for the plugin (e.g.: reference value for an application execution, the url for the service that will provide me the metrics or the path to the log file I need to read to capture the metrics and the host ip where this log is located).

* **monitoring_application(self)**
	* This method does every necessary step to calculate or capture the metric that must be published. If the metric will be stored into monasca, you must create an object monitor.monasca.manager.MonascaMonitor and use send_metrics([metrics]) to publish the metrics, where [metrics] is a list with the metrics you want to push into monasca and each metric is a dictionary with this following structure:
		* ```
			metric = {'name':  'application-name.metric-namer'
			   'value': value
			   'timestamp': time.time() * 1000
			   'dimensions': self.dimensions
		  ```
		   
* **Example**:

	* ```
		class MyNewMonitor:

    		def __init__(self, app_id, plugin_info, collect_period, retries=100):
        	# set things up
        
    		def monitoring_application(self):
        	# monitoring logic
        	pass
	  ```

2. Edit the MonitorBuilder class adding a new condition to check the plugin name in the start_monitor. Instantiate the plugin in the conditional case.
* **Example**:
	* ```
		...
		elif plugin_name == "mynewmonitor":
	            plugin = MyNewMonitor(app_id, plugin_info, collect_period, retries=retries)
		...
		```
