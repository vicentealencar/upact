from datetime import datetime, time
from unittest import TestCase
from upact.models import PlaytimeRule

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
