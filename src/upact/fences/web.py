import dns.resolver
import logging
import time

import peewee as pw

import config

from upact.models import Uri, BlockedIp, PlaytimeRule, database_proxy
import upact.networking as networking

from datetime import datetime, timedelta


_RUNNING = False


def permanently_blocked_ips(db, current_time=datetime.now(), networking=networking):
    return list(BlockedIp.select().join(Uri).where(Uri.type_uri == Uri.TYPE_PERMANENTLY_BLOCKED_IP))


def ips_to_unblock(db, current_time=datetime.now(), networking=networking):
    all_urls = [uri for uri in Uri.select().where(Uri.type_uri == 'url')]

    urls_to_unblock = [uri for uri in all_urls if uri.is_active(when=current_time, now_date=current_time)]

    ips_to_unblock = [ip for url in urls_to_unblock for ip in url.ips]
    ips_to_unblock += [ip for ip in BlockedIp.select().where(BlockedIp.uri.is_null())]
    ips_to_unblock += [ip for ip in BlockedIp.select().join(Uri).where((Uri.type_uri == Uri.TYPE_URL) & (BlockedIp.updated_at <= current_time - timedelta(hours=config.IP_EXPIRY_TIME)))]

    return ips_to_unblock


def unblock_ips(db, current_time=datetime.now(), networking=networking):
    target_ips = ips_to_unblock(db, current_time, networking)

    for ip in target_ips:
        ip.delete_instance()

    return target_ips

def blocked_ips_from_urls(db, current_time=datetime.now(), networking=networking):

    logging.info("Getting URLs from database")

    all_urls = [uri for uri in Uri.select().where(Uri.type_uri == 'url')]
    urls_to_block = [uri for uri in all_urls if not uri.is_active(when=current_time, now_date=current_time)]

    logging.info("DNS querying urls...")

    ips_to_block = []
    for url in urls_to_block:
        try:
            ips_v4, ips_v6 = networking.dns_lookup(url.name)
            ips_v4 = {(ip, 4) for ip in ips_v4}
            ips_v6 = {(ip, 6) for ip in ips_v6}
            all_ips = ips_v4 | ips_v6

            for (ip, version) in all_ips:
                blocked_ip = BlockedIp.get_or_none(BlockedIp.address==ip, BlockedIp.uri==url, BlockedIp.version==version)

                if blocked_ip:
                    blocked_ip.updated_at = current_time
                    blocked_ip.save()
                else:
                    blocked_ip = BlockedIp.create(
                            address=ip,
                            uri=url,
                            version=version,
                            created_at=current_time,
                            updated_at=current_time)

                ips_to_block.append(blocked_ip)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as ex:
            logging.error(ex.msg)


    logging.info("Done querying URLs")

    return ips_to_block


def start_service(platform, db, debug=False, current_time=datetime.now(), networking=networking):
    global _RUNNING
    _RUNNING = True

    platform.update_permanently_blocked_ips(permanently_blocked_ips(db, current_time=current_time, networking=networking))

    while _RUNNING:
        platform.update_ips_from_urls(
            ips_to_block=blocked_ips_from_urls(db, current_time=current_time, networking=networking),
            ips_to_unblock=unblock_ips(db, current_time=current_time, networking=networking))

        if debug:
            break

        time.sleep(5 * 60)

def stop_service():
    global _RUNNING
    _RUNNING = False
