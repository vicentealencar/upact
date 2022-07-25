from subprocess import CalledProcessError

from unittest import TestCase
from unittest.mock import Mock, patch

from upact.models import BlockedIp
from upact.platforms.windows import Windows

class WindowsPlatformTests(TestCase):

    def _verify_rules_removed(self, windows, call_mock, check_output_mock, ips_to_block=[]):
        check_output_mock.return_value = b'upact 151.101.1.140                                                                                                                                                                  \r\nupact 151.101.129.140                                                                                                                                                                \r\n'
        windows.update_firewall(ips_to_block=ips_to_block, ips_to_unblock=[], config=None)

        self.assertEqual(call_mock.call_args_list[0].args[0], 'netsh advfirewall firewall delete rule name="upact 151.101.1.140"')
        self.assertEqual(call_mock.call_args_list[1].args[0], 'netsh advfirewall firewall delete rule name="upact 151.101.129.140"')

    @patch("subprocess.check_output")
    @patch("subprocess.call")
    def test_existing_rules_removed(self, call_mock, check_output_mock):

        windows = Windows()

        self._verify_rules_removed(windows, call_mock, check_output_mock)


    @patch("subprocess.check_output")
    @patch("subprocess.call")
    def test_rules_removed_and_added(self, call_mock, check_output_mock):

        windows = Windows()

        self._verify_rules_removed(windows,
                call_mock,
                check_output_mock,
                ips_to_block=[BlockedIp(address='200.253.245.1'), BlockedIp(address='200.253.236.1')])

        self.assertEqual(call_mock.call_args_list[2].args[0],
            'netsh advfirewall firewall add rule name="upact 200.253.245.1" dir=out action=block remoteip=200.253.245.1')
        self.assertEqual(call_mock.call_args_list[3].args[0],
                'netsh advfirewall firewall add rule name="upact 200.253.236.1" dir=out action=block remoteip=200.253.236.1')

    @patch("subprocess.check_output")
    @patch("subprocess.call")
    def test_no_rules_removed(self, call_mock, check_output_mock):

        windows = Windows()

        check_output_mock.side_effect = CalledProcessError(1, "")
        windows.update_firewall(ips_to_block=[], ips_to_unblock=[], config=None)

        self.assertEqual(call_mock.call_count, 0)
