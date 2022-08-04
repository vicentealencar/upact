import datetime
import peewee as pw
import upact.store.uri

from upact import store
from upact.models import Uri, PlaytimeRule, BlockedIp, database_proxy

from unittest import TestCase

class UriStoreTests(TestCase):

    def setUp(self):
        self.db = pw.SqliteDatabase(":memory:")
        self.db.connect()
        database_proxy.initialize(self.db)
        database_proxy.create_tables([Uri, PlaytimeRule, BlockedIp])

    def tearDown(self):
        self.db.close()

    def test_block_single(self):
        store.uri.block(["google.com"])
        self.assertEqual({ uri.name for uri in Uri.select() }, {"google.com"})

    def test_block_multiple(self):
        store.uri.block(["google.com", "facebook.com"])
        self.assertEqual({ uri.name for uri in Uri.select() }, {"google.com", "facebook.com"})

    def test_block_single_with_playtime(self):
        store.uri.block(["google.com"], playtime_days="every day", playtime_hours=[["14:00", "15:00"], ["18:00", "19:00"]])

        uri = [uri for uri in Uri.select()][0]
        self.assertEqual(uri.name, "google.com")
        self.assertEqual(uri.playtime_rules[0].from_time, datetime.time(14, 00))
        self.assertEqual(uri.playtime_rules[0].to_time, datetime.time(15, 00))
        self.assertEqual(uri.playtime_rules[0].frequency, "every day")

        self.assertEqual(uri.playtime_rules[1].from_time, datetime.time(18, 00))
        self.assertEqual(uri.playtime_rules[1].to_time, datetime.time(19, 00))
        self.assertEqual(uri.playtime_rules[1].frequency, "every day")

    def test_block_invalid_playtime_days(self):
        try:
            store.uri.block(["google.com"], playtime_days="every brazilian carnival", playtime_hours=[["14:00", "15:00"], ["18:00", "19:00"]])
            assert False
        except ValueError as e:
            assert True

    def test_remove(self):
        self.test_block_multiple()

        store.uri.remove(["facebook.com"])
        self.assertEqual({ uri.name for uri in Uri.select() }, {"google.com"})

    def test_remove_with_playtime(self):
        self.test_block_single_with_playtime()
        store.uri.block(["facebook.com"])

        store.uri.remove(["google.com"])
        self.assertEqual({ uri.name for uri in Uri.select() }, {"facebook.com"})
        self.assertEqual({ pt for pt in PlaytimeRule.select() }, set())

    def test_list(self):
        store.uri.block(["google.com", "facebook.com"])
        self.assertEqual({uri.name for uri in store.uri.list()}, {"google.com", "facebook.com"})

    def test_list_multiple_uri_types(self):
        store.uri.block(["google.com", "facebook.com"])
        store.uri.block(["starcraft"], type_uri=Uri.TYPE_APP)

        self.assertEqual({uri.name for uri in store.uri.list()}, {"google.com", "facebook.com", "starcraft"})

    def test_list_single_uri_type(self):
        store.uri.block(["google.com", "facebook.com"])
        store.uri.block(["starcraft"], type_uri=Uri.TYPE_APP)

        self.assertEqual({uri.name for uri in store.uri.list(type_uri=Uri.TYPE_URL)}, {"google.com", "facebook.com"})
        self.assertEqual({uri.name for uri in store.uri.list(type_uri=Uri.TYPE_APP)}, {"starcraft"})
