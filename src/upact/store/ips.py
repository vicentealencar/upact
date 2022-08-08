from upact.models import BlockedIp


def list():
    return BlockedIp.select()


def block(ips_to_block, uri):

    saved_ips = []
    for ip_address in ips_to_block:
        blocked_ip = BlockedIp(address=ip_address, uri=uri)
        blocked_ip.save()
        saved_ips.append(blocked_ips)

    return saved_ips


def remove(ips_to_remove):
    for ip_address in ips_to_remove:
        for ip in BlockedIp.select().where(BlockedIp.address == ip_address):
            ip.delete_instance()
