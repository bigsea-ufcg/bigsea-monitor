import ConfigParser
import mock
import unittest

from monitor.monasca.manager import MonascaMonitor


class TestManager(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('ConfigParser.RawConfigParser')
    @mock.patch('monitor.monasca.manager.MonascaMonitor._get_monasca_client')
    def test_init_manager(self, config_mock, monasca_mock):
        MonascaMonitor()
        config_mock.assert_called_once_with()
        monasca_mock.assert_called_once_with()

    @mock.patch('monitor.monasca.manager.MonascaMonitor._get_monasca_client')
    def test_get_measurements(self, monasca_mock):
        ConfigParser.RawConfigParser = mock.Mock()
        m = MonascaMonitor()
        m.get_measurements(None, None)
        monasca_mock.assert_called_once_with()
