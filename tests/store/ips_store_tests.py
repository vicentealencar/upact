import peewee as pw
import upact.store.ips

from upact import store
from upact.models import Uri, BlockedIp, database_proxy

from unittest import TestCase

class IpsStoreTests(TestCase):

    def setUp(self):
        self.db = pw.SqliteDatabase(":memory:")
        self.db.connect()
        database_proxy.initialize(self.db)
        database_proxy.create_tables([BlockedIp, Uri])

    def tearDown(self):
        self.db.close()

    def test_block_single_ipv4(self):
        store.ips.block(["200.253.245.1"], uri=Uri.permanently_blocked_ips_uri())
        ips = [ip for ip in store.ips.list()]

        self.assertEqual(len(ips), 1)
        self.assertEqual(ips[0].version, 4)
        self.assertEqual(ips[0].address, "200.253.245.1")

    def test_block_single_ipv6(self):
        store.ips.block(["2001:4998:44:3507::8001"], uri=Uri.permanently_blocked_ips_uri())
        ips = [ip for ip in store.ips.list()]

        self.assertEqual(len(ips), 1)
        self.assertEqual(ips[0].version, 6)
        self.assertEqual(ips[0].address, "2001:4998:44:3507::8001")

    def test_block_multiple(self):
        store.ips.block(["2001:4998:44:3507::8001", "200.253.245.1"], uri=Uri.permanently_blocked_ips_uri())
        ips = [ip for ip in store.ips.list()]

        self.assertEqual(len(ips), 2)
        self.assertEqual(ips[0].version, 6)
        self.assertEqual(ips[0].address, "2001:4998:44:3507::8001")

        self.assertEqual(ips[1].version, 4)
        self.assertEqual(ips[1].address, "200.253.245.1")

    def test_remove(self):
        self.test_block_multiple()

        store.ips.remove(["200.253.245.1"])

        ips = [ip for ip in store.ips.list()]

        self.assertEqual(len(ips), 1)
        self.assertEqual(ips[0].version, 6)
        self.assertEqual(ips[0].address, "2001:4998:44:3507::8001")

    def test_remove_all(self):
        self.test_block_multiple()

        store.ips.remove(["200.253.245.1", "2001:4998:44:3507::8001"])

        ips = [ip for ip in store.ips.list()]

        self.assertEqual(ips, [])

    def test_invalid_ip(self):
        try:
            store.ips.block(["200.253.245.1.3"], uri=Uri.permanently_blocked_ips_uri())
            assert False
        except ValueError as ex:
            assert True
