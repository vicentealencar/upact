from upact.models import BlockedIp


def list():
    return BlockedIp.select()
