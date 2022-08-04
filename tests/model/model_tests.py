import peewee as pw

from datetime import datetime, time
from unittest import TestCase
from upact.models import PlaytimeRule, BlockedIp, Uri, database_proxy

class ModelTests(TestCase):

    def test_playtime_rule_active(self):
        rule = PlaytimeRule(from_time=time(12, 0), to_time=time(16, 0), frequency="every day")
        test_date = datetime(2021, 1, 1, 14, 0)
        self.assertTrue(rule.is_active(when=test_date, now_date=test_date))

    def test_playtime_rule_not_active_hour_earlier(self):
        rule = PlaytimeRule(from_time=time(12, 0), to_time=time(16, 0), frequency="every day")
        test_date = datetime(2021, 1, 1, 11, 0)
        self.assertFalse(rule.is_active(when=test_date, now_date=test_date))

    def test_playtime_rule_not_active_hour_lower_bound(self):
        rule = PlaytimeRule(from_time=time(12, 0), to_time=time(16, 0), frequency="every day")
        test_date = datetime(2021, 1, 1, 12, 0)
        self.assertTrue(rule.is_active(when=test_date, now_date=test_date))

    def test_playtime_rule_not_active_hour_later(self):
        rule = PlaytimeRule(from_time=time(12, 0), to_time=time(16, 0), frequency="every day")
        test_date = datetime(2021, 1, 1, 16, 1)
        self.assertFalse(rule.is_active(when=test_date, now_date=test_date))

    def test_playtime_rule_not_active_hour_upper_bound(self):
        rule = PlaytimeRule(from_time=time(12, 0), to_time=time(16, 0), frequency="every day")
        test_date = datetime(2021, 1, 1, 16, 0)
        self.assertFalse(rule.is_active(when=test_date, now_date=test_date))

    def test_playtime_rule_not_active_day(self):
        rule = PlaytimeRule(from_time=time(12, 0), to_time=time(16, 0), frequency="every weekend")
        test_date = datetime(2021, 1, 1, 15, 1)
        self.assertFalse(rule.is_active(when=test_date, now_date=test_date))

    def test_comparing_same_blocked_ip(self):
        uri1 = Uri(name="www.google.com")
        uri2 = Uri(name="www.microsoft.com")
        ip1 = BlockedIp(address="200.253.245.1", uri=uri1, version=4)
        ip2 = BlockedIp(address="200.253.245.1", uri=uri2, version=4)

        self.assertEqual(ip1, ip2)

    def test_invalid_playtime_frequency_raises(self):
        self.db = pw.SqliteDatabase(":memory:")
        self.db.connect()
        database_proxy.initialize(self.db)
        database_proxy.create_tables([Uri, PlaytimeRule])

        uri = Uri(name="google.com")
        uri.save()

        rule = PlaytimeRule(from_time=time(12, 0), to_time=time(16, 0), frequency="every brazilian carnival", uri=uri)

        try:
            rule.save()
            assert False
        except ValueError as e:
            assert True
