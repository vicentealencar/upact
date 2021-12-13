import peewee as pw

import upact.platforms
import web_fence

from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from upact.models import *

class WebFenceTests(TestCase):

    def setUp(self):
        self.db = pw.SqliteDatabase(":memory:")
        self.db.connect()
        database_proxy.initialize(self.db)
        database_proxy.create_tables([Uri, PlaytimeRule, BlockedIp])

        self.test_uri = Uri(name="www.google.com")
        self.test_uri.save()

        self.rule1 = PlaytimeRule(from_time="14:00", to_time="18:00", frequency="every day", uri=self.test_uri)
        self.rule1.save()

    def tearDown(self):
        self.db.close()

    def test_site_blocked(self):
        networking_mock = Mock()
        networking_mock.dns_lookup.side_effect = [({'200.253.245.1'}, {'2345:0425:2CA1:0000:0000:0567:5673:23b5'})]
        ips_to_block, ips_to_unblock = web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 11, 0, 0),
                networking=networking_mock)

        self.assertEqual({ip.address for ip in ips_to_block}, {'200.253.245.1', '2345:0425:2CA1:0000:0000:0567:5673:23b5'})
        self.assertEqual({ip.version for ip in ips_to_block}, {4, 6})

    def test_block_same_ip_twice(self):
        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = ({'200.253.245.1'}, {'2345:0425:2CA1:0000:0000:0567:5673:23b5'})
        web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 11, 0, 0),
                networking=networking_mock)

        # Calling twice to trigger blocking the same ip again
        web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 11, 0, 0),
                networking=networking_mock)

        all_blocked_ips = {bip.address for bip in BlockedIp.select()}

        self.assertEqual(len(all_blocked_ips), 2)
        self.assertEqual(all_blocked_ips, {'200.253.245.1', '2345:0425:2CA1:0000:0000:0567:5673:23b5'})

    def test_playtime_rule_active(self):
        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = ({'200.253.245.1'},)
        ips_to_block, ips_to_unblock = web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 15, 0, 0),
                networking=networking_mock)

        self.assertEqual(ips_to_block, [])

    def test_multiple_playtime_rules_active(self):
        rule2 = PlaytimeRule(from_time="09:00", to_time="10:00", frequency="every day", uri=self.test_uri)
        rule2.save()
        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = ({'200.253.245.1'}, set())
        ips_to_block, ips_to_unblock = web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 9, 30, 0),
                networking=networking_mock)

        self.assertEqual(ips_to_block, [])

    def test_multiple_playtime_rules_inactive(self):
        rule2 = PlaytimeRule(from_time="09:00", to_time="10:00", frequency="every day", uri=self.test_uri)
        rule2.save()
        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = ({'200.253.245.1'}, set())
        ips_to_block, ips_to_unblock = web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 8, 0, 0),
                networking=networking_mock)

        self.assertEqual([ip.address for ip in ips_to_block], ['200.253.245.1'])

    def test_ips_clear_daily(self):
        upact.platforms['Test'] = Mock()
        networking_mock = Mock()

        networking_mock.dns_lookup.return_value = ({'200.253.245.1'}, set())
        web_fence.update_ip_rules(
            self.db,
            current_platform='Test',
            networking=networking_mock,
            current_time=datetime(2021, 12, 1, 7, 0, 0))

        self.assertEqual(len([ip for ip in BlockedIp.select()]), 1)

        networking_mock.dns_lookup.return_value = ({'200.253.245.2'}, set())
        web_fence.update_ip_rules(
            self.db,
            current_platform='Test',
            networking=networking_mock,
            current_time=datetime(2021, 12, 2, 8, 0, 0))

        all_ips = [ip for ip in BlockedIp.select()]
        self.assertEqual(len(all_ips), 1)


    def test_ip_clears_when_playtime_activates(self):
        upact.platforms['Test'] = Mock()

        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = ({'200.253.245.1'}, set())
        web_fence.update_ip_rules(
                self.db,
                current_platform='Test',
                current_time=datetime(2021, 12, 1, 8, 30, 0),
                networking=networking_mock)

        self.assertEqual(len([ip for ip in BlockedIp.select()]), 1)

        networking_mock.dns_lookup.return_value = ({'200.253.245.1'}, set())
        web_fence.update_ip_rules(
                self.db,
                current_platform='Test',
                current_time=datetime(2021, 12, 1, 17, 0, 0),
                networking=networking_mock)

        self.assertEqual(len([ip for ip in BlockedIp.select()]), 0)

    def test_ip_stays_blocked_after_24h(self):
        upact.platforms['Test'] = Mock()

        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = ({'200.253.245.1'}, set())
        web_fence.update_ip_rules(
                self.db,
                current_platform='Test',
                current_time=datetime(2021, 12, 1, 8, 30, 0),
                networking=networking_mock)

        self.assertEqual(len([ip for ip in BlockedIp.select()]), 1)

        networking_mock.dns_lookup.return_value = ({'200.253.245.1'}, set())
        web_fence.update_ip_rules(
                self.db,
                current_platform='Test',
                current_time=datetime(2021, 12, 2, 8, 45, 0),
                networking=networking_mock)

        self.assertEqual(len([ip for ip in BlockedIp.select()]), 1)

    def test_ip_blocking_by_platform(self):
        upact.platforms['Test'] = Mock()

        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = ({'200.253.245.1'}, set())

        web_fence.update_ip_rules(
            self.db,
            current_platform='Test',
            networking=networking_mock,
            current_time=datetime(2021, 12, 1, 7, 0, 0))

        ips_to_block = {ip.address for ip in upact.platforms['Test'].update_firewall.call_args[0][0]}

        self.assertEqual(ips_to_block, {'200.253.245.1'})

    def test_ips_without_uri_unblocked(self):
        upact.platforms['Test'] = Mock()

        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = ({'200.253.245.1'}, set())

        web_fence.update_ip_rules(
            self.db,
            current_platform='Test',
            networking=networking_mock,
            current_time=datetime(2021, 12, 1, 7, 0, 0))

        self.test_uri.delete_instance(recursive=True)

        web_fence.update_ip_rules(
            self.db,
            current_platform='Test',
            networking=networking_mock,
            current_time=datetime(2021, 12, 1, 7, 5, 0))

        update_firewall_call = upact.platforms['Test'].update_firewall.call_args[0]
        ips_to_block = update_firewall_call[0]
        ips_to_unblock = update_firewall_call[1]

        self.assertEqual(ips_to_block, [])
        self.assertEqual(ips_to_unblock[0].address, '200.253.245.1')
