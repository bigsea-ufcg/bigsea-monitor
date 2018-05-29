# Description
On the process of executing an application, the monitor service is responsible for managing all the needed steps to gather metrics from the application and/or its infrastructure and publish it in any existing storage, which should be located, for example, in the cloud monitoring service (as Monasca in Openstack infrastructure) or in a local machine (Broker Kubernetes plugin uses Redis for monitoring).
The goal of this metric translation is to enable other components in the framework (e.g., the controller) to be generic, while still being able to process QoS metrics for the application and take decisions based on these metrics.
The monitor service is initiated by the broker, which provides the plugin type that must be used and some basic informations about the application and the infrastructure (e.g., application id, cluster address, etc).
That is, the broker decides what kind of monitoring will be performed for each application based on the submission information.

# Architecture
The monitor is implemented following a plugin architecture, allowing the framework to monitor different types of application and different metrics of interest related to the QoS of the applications.
The plugin architecture allows the implementation of monitors with different goals, providing flexibility between the framework and monitored application (e.g., plugins to capture specific metrics from the application execution, as application progress, and others about consumption of allocated resources to the application).
