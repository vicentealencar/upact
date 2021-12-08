import dns.resolver
import logging
import platform

import peewee as pw

import config

from upact.models import *
import upact.networking as networking
import upact.platforms

from datetime import datetime


def generate_ips(db, current_time=datetime.now(), networking=networking):

    all_urls = [uri for uri in Uri.select().where(Uri.type_uri == 'url')]
    urls_to_block = [uri for uri in all_urls if not uri.is_active(when=current_time, now_date=current_time)]
    urls_to_unblock = [uri for uri in all_urls if uri.is_active(when=current_time, now_date=current_time)]

    for url in urls_to_unblock:
        for ip in url.ips:
            ip.delete_instance()

    if current_time.hour == 15 and current_time.minute <= 10:
        BlockedIp.truncate_table()

    for url in urls_to_block:
        try:
            for ip in networking.dns_lookup(url.name):
                BlockedIp.get_or_create(address=ip, uri=url)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as ex:
            logging.error(ex.msg)

    return set([ip.address for ip in BlockedIp.select()])


def block_ips(db, current_platform=platform.system(), config=config, current_time=datetime.now(), networking=networking):
    ips_to_block = generate_ips(db, current_time=current_time, networking=networking)
    upact.platforms[current_platform].block_ips(ips_to_block, config)


def run():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info("Running upact web")

    db = pw.SqliteDatabase(config.DATABASE_FILE)
    db.connect()
    database_proxy.initialize(db)

    block_ips(db)


if __name__ == "__main__":
    run()
