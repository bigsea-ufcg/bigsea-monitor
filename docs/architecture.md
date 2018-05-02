# Architecture description
The monitor is implemented following a plugin architecture, allowing the framework to monitor different types of application and different metrics of interest related to the QoS of the applications.
The plugin architecture allows the implementation of monitors with different goals, providing flexibility between the framework and monitored application (e.g., plugins to capture specific metrics from the application execution, as application progress, and others about consumption of allocated resources to the application).
The monitor service is initiated by the broker, which provides the plugin type that must be used and some basic informations about the application and the infrastructure (e.g., application id, cluster address, etc).
That is, the broker decides what kind of monitoring will be performed for each application based on the submission information.
