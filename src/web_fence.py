import dns.resolver
import os
import subprocess
import logging

from upact.models import *
import peewee as pw

import config
import upact.networking as networking

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


def block_ips(ips_to_block):

    with open(config.PF_CONF_TEMPLATE, "r") as etc_pf:
        pf_conf = etc_pf.read()

    with open(config.BLOCKED_IPS_FILE, "w") as blocked_ips_file:
        blocked_ips_file.write("\n".join(ips_to_block))

    pf_conf += 'table <blocked_ips> persist file "{0}"'.format(os.path.join(os.getcwd(), config.BLOCKED_IPS_FILE))
    pf_conf += "\n"

    pf_conf += "block return from any to <blocked_ips>"
    pf_conf += "\n"

    with open(config.PF_CONF_PATH, "w+") as pf_conf_file:
        pf_conf_file.write(pf_conf)

    subprocess.call(["sudo", "pfctl", "-E", "-f", config.PF_CONF_PATH])


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info("Running upact web")

    db = pw.SqliteDatabase(config.DATABASE_FILE)
    db.connect()
    database_proxy.initialize(db)
    ips_to_block = generate_ips(db)
    block_ips(ips_to_block)
