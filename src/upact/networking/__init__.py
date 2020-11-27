import dns.resolver
import ipaddress


def global_unicast_address(ipv6):
    return ":".join(ipv6.split(":")[0:3]) + "::/48"


def global_unicast_address_list(ip_list):
    return [global_unicast_address(ip) if ipaddress.ip_address(ip).version == 6 else ip for ip in ip_list]
    

def dns_lookup(name):
    ipv4_result = map(lambda x: x.address, dns.resolver.query(name, "A"))
    try:
        ipv6_result = map(lambda x: x.address, dns.resolver.query(name, "AAAA"))
    except dns.resolver.NoAnswer as ex:
        print(ex.msg)
        ipv6_result = []

    return set(ipv4_result) | set(ipv6_result)

