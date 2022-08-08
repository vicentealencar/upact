import ipaddress
from upact.models import BlockedIp


def list():
    return BlockedIp.select()


def block(ips_to_block, uri):

    saved_ips = []
    for ip_address in ips_to_block:
        blocked_ip = BlockedIp(address=ip_address, uri=uri, version=ipaddress.ip_address(ip_address).version)
        blocked_ip.save()
        saved_ips.append(blocked_ip)

    return saved_ips


def remove(ips_to_remove):
    for ip_address in ips_to_remove:
        for ip in BlockedIp.select().where(BlockedIp.address == ip_address):
            ip.delete_instance()
