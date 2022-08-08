import argparse
import shlex

from unittest import TestCase
from unittest.mock import Mock, patch

from upact.cmdline.subcommands.ips import sub_parser
from upact.models import BlockedIp, Uri

class IpsCmdlineTests(TestCase):
    
    def setUp(self):
        self.main_parser = argparse.ArgumentParser()
        self.subparsers = self.main_parser.add_subparsers()
        self.parser = sub_parser(self.subparsers)

    @patch("upact.store.ips.list")
    def test_listing(self, list_ips):
        result = self.parser.parse_args(shlex.split('--list'))

        uri = Mock()
        uri.name = "facebook.com"
        uri.type_uri = Uri.TYPE_URL

        ip1 = Mock()
        ip1.address = "200.253.245.1"
        ip1.uri = uri
        ip1.version = 4

        ip2 = Mock()
        ip2.address = "200.253.236.1"
        ip2.uri = uri
        ip2.version = 4

        list_ips.return_value = [ip1, ip2]

        command = result.init_command(result)
        command()

        list_ips.assert_called_once_with()
        self.assertEqual(command.display_string, '+--------------+---------------+\n| Url          |      Ips      |\n+--------------+---------------+\n| facebook.com | 200.253.245.1 |\n|              | 200.253.236.1 |\n+--------------+---------------+')
