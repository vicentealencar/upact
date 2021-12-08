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
        networking_mock.dns_lookup.side_effect = [{'200.253.245.1'}]
        ips_to_block = web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 11, 0, 0),
                networking=networking_mock)

        self.assertEqual(ips_to_block, {'200.253.245.1'})

    def test_block_same_ip_twice(self):
        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = {'200.253.245.1'}
        web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 11, 0, 0),
                networking=networking_mock)

        # Calling twice to trigger blocking the same ip again
        web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 11, 0, 0),
                networking=networking_mock)

        all_blocked_ips = [bip for bip in BlockedIp.select()]

        self.assertEqual(len(all_blocked_ips), 1)
        self.assertEqual(all_blocked_ips[0].address, '200.253.245.1')

    def test_playtime_rule_active(self):
        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = {'200.253.245.1'}
        ips_to_block = web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 15, 0, 0),
                networking=networking_mock)

        self.assertEqual(ips_to_block, set())

    def test_multiple_playtime_rules_active(self):
        rule2 = PlaytimeRule(from_time="09:00", to_time="10:00", frequency="every day", uri=self.test_uri)
        rule2.save()
        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = {'200.253.245.1'}
        ips_to_block = web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 9, 30, 0),
                networking=networking_mock)

        self.assertEqual(ips_to_block, set())

    def test_multiple_playtime_rules_inactive(self):
        rule2 = PlaytimeRule(from_time="09:00", to_time="10:00", frequency="every day", uri=self.test_uri)
        rule2.save()
        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = {'200.253.245.1'}
        ips_to_block = web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 8, 0, 0),
                networking=networking_mock)

        self.assertEqual(ips_to_block, {'200.253.245.1'})

    def test_ips_clear_daily(self):
        networking_mock = Mock()

        networking_mock.dns_lookup.return_value = {'200.253.245.1'}
        web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 8, 30, 0),
                networking=networking_mock)

        networking_mock.dns_lookup.return_value = {'200.253.245.1'}
        web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 15, 5, 0),
                networking=networking_mock)

        all_blocked_ips = [bip for bip in BlockedIp.select()]
        self.assertEqual(len(all_blocked_ips), 0)

    def test_ip_clears_when_playtime_activates(self):
        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = {'200.253.245.1'}
        blocked_ips = web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 8, 30, 0),
                networking=networking_mock)

        self.assertEqual(len(blocked_ips), 1)

        networking_mock.dns_lookup.return_value = {'200.253.245.1'}
        blocked_ips = web_fence.generate_ips(
                self.db,
                current_time=datetime(2021, 12, 1, 17, 0, 0),
                networking=networking_mock)

        self.assertEqual(len(blocked_ips), 0)

    def test_ip_blocking_by_platform(self):
        upact.platforms['Test'] = Mock()

        networking_mock = Mock()
        networking_mock.dns_lookup.return_value = {'200.253.245.1'}

        web_fence.block_ips(
            self.db,
            current_platform='Test',
            networking=networking_mock,
            current_time=datetime(2021, 12, 1, 7, 0, 0))

        self.assertEqual(upact.platforms['Test'].block_ips.call_args[0][0], {'200.253.245.1'})
