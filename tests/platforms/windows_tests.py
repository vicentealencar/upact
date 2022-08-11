from subprocess import CalledProcessError

from unittest import TestCase
from unittest.mock import Mock, patch

from upact.models import BlockedIp
from upact.platforms.windows import Windows

class WindowsPlatformTests(TestCase):

    def _verify_rules_removed(self, windows, call_mock, ips_to_block=[]):
        windows.create_firewall_rule(ips_to_block=ips_to_block, rule_name="upact test")

        self.assertEqual(call_mock.call_args_list[0].args[0], 'netsh advfirewall firewall delete rule name="upact test"')

    @patch("subprocess.Popen")
    @patch("subprocess.call")
    def test_existing_rules_removed(self, call_mock, popen_mock):

        windows = Windows(Mock())

        self._verify_rules_removed(windows, call_mock)

        self.assertEqual(popen_mock.call_count, 0)


    @patch("subprocess.Popen")
    @patch("subprocess.call")
    def test_rules_removed_and_added(self, call_mock, popen):

        windows = Windows(Mock())

        process_mock = Mock()
        popen().__enter__.return_value = process_mock

        self._verify_rules_removed(windows,
                call_mock,
                ips_to_block=[BlockedIp(address='200.253.245.1'), BlockedIp(address='200.253.236.1')])

        write_mock = process_mock.stdin.write

        self.assertEqual(write_mock.call_args_list[0][0][0], b'$ips_to_block = @()\n')
        self.assertEqual(write_mock.call_args_list[1][0][0], b'$ips_to_block += "200.253.245.1"\n')
        self.assertEqual(write_mock.call_args_list[2][0][0], b'$ips_to_block += "200.253.236.1"\n')
        self.assertEqual(write_mock.call_args_list[3][0][0], b'New-NetFirewallRule -DisplayName "upact test" -Direction Outbound -Action Block -RemoteAddress $ips_to_block\n')
