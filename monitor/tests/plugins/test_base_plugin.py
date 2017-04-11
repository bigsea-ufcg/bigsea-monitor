import mock
import unittest

from monitor.plugins.base import Plugin

class TestPluginBase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init_empty_plugin(self):
        plugin_1 = Plugin(3)
        plugin_2 = Plugin(3)

        self.assertNotEqual(plugin_1, plugin_2)
        self.assertFalse(plugin_1.running)
        self.assertEqual(plugin_1.dimensions, {})
        self.assertEqual(plugin_1.collect_period, 3)
        self.assertEqual(plugin_1.attempts, 30)
        self.assertEqual(plugin_1.app_id, None)

        self.assertFalse(plugin_2.running)
        self.assertEqual(plugin_2.dimensions, {})
        self.assertEqual(plugin_2.collect_period, 3)
        self.assertEqual(plugin_2.attempts, 30)
        self.assertEqual(plugin_2.app_id, None)

    def test_start_plugin(self):
        pass

