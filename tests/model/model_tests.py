import peewee as pw

from datetime import datetime, time
from unittest import TestCase
from upact.models import PlaytimeRule, BlockedIp, Uri, database_proxy

class ModelTests(TestCase):

    def init_db(self):
        self.db = pw.SqliteDatabase(":memory:")
        self.db.connect()
        database_proxy.initialize(self.db)
        database_proxy.create_tables([Uri, PlaytimeRule])

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
        self.init_db()

        uri = Uri(name="google.com")
        uri.save()

        rule = PlaytimeRule(from_time=time(12, 0), to_time=time(16, 0), frequency="every brazilian carnival", uri=uri)

        try:
            rule.save()
            assert False
        except ValueError as e:
            assert True

    def test_duplicate_name_raises(self):
        self.init_db()

        Uri(name="google.com").save()

        try:
            Uri(name="google.com").save()
        except pw.IntegrityError as e:
            assert True
            
    def test_duplicate_name_different_type(self):
        self.init_db()

        Uri(name="google.com").save()

        Uri(name="google.com", type_uri=Uri.TYPE_APP).save()

    def test_permanently_blocked_ips_singleton(self):
        self.init_db()

        self.assertEqual([uri for uri in Uri.select().where(Uri.type_uri == Uri.TYPE_PERMANENTLY_BLOCKED_IP)], [])

        Uri.permanently_blocked_ips_uri()

        permanently_blocked_uris = [uri for uri in Uri.select().where(Uri.type_uri == Uri.TYPE_PERMANENTLY_BLOCKED_IP)]

        self.assertEqual(len(permanently_blocked_uris), 1)
        self.assertEqual(permanently_blocked_uris[0].name, "Permanently blocked Ip")
        self.assertEqual(permanently_blocked_uris[0].type_uri, Uri.TYPE_PERMANENTLY_BLOCKED_IP)
