from plugins.spark_progress import SparkProgress


class Monitor:

    def __init__(self):
        self.app_monitored = {}

    def start_monitor(self, plugin_name, info_plugin):

        plugin = None

        if plugin_name == "spark_progress":
            plugin = SparkProgress(info_plugin)
            self.app_monitored[info_plugin['spark_id']] = plugin

        print plugin.getName()

        plugin.start()

    def kill_monitor(self, app_id):
        try:
            self.app_monitored.pop(app_id, None).stop()
        except Exception as ex:
            ex.message
            pass
