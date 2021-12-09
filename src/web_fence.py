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

    if current_time.hour == 15 and current_time.minute <= 10:
        BlockedIp.truncate_table()

    ips_to_block = []
    for url in urls_to_block:
        try:
            ips_v4, ips_v6 = networking.dns_lookup(url.name)
            ips_v4 = {(ip, 4) for ip in ips_v4}
            ips_v6 = {(ip, 6) for ip in ips_v6}
            all_ips = ips_v4 | ips_v6

            for (ip, version) in all_ips:
                ips_to_block.append(BlockedIp.get_or_create(address=ip, uri=url, version=version)[0])
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as ex:
            logging.error(ex.msg)

    ips_to_unblock = [ip for url in urls_to_unblock for ip in url.ips]

    return (ips_to_block, ips_to_unblock)


def update_ip_rules(db, current_platform=platform.system(), config=config, current_time=datetime.now(), networking=networking):
    ips_to_block, ips_to_unblock = generate_ips(db, current_time=current_time, networking=networking)
    upact.platforms[current_platform].update_firewall(ips_to_block, ips_to_unblock, config)

    for ip in ips_to_unblock:
        ip.delete_instance()



def run():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info("Running upact web")

    db = pw.SqliteDatabase(config.DATABASE_FILE)
    db.connect()
    database_proxy.initialize(db)

    update_ip_rules(db)


if __name__ == "__main__":
    run()
