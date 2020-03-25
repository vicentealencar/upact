import dns.resolver

def global_unicast_address(ipv6):
    return ":".join(x.split(":")[0:3]) + "::/48"

def global_unicast_address_list(ip_list):
    [global_unicast_address(ip) if ipaddress.ip_address(ip).version == 6 else ip for ip in ip_list]
    

def dns_lookup(name):
    ipv4_result = map(lambda x: x.address, dns.resolver.query(name, "A"))
    try:
        ipv6_result = map(lambda x: x.address, dns.resolver.query(name, "AAAA"))
    except dns.resolver.NoAnswer as ex:
        print(ex.msg)
        ipv6_result = []
    ipv6_unicast = list(map(lambda x: ":".join(x.split(":")[0:3]) + "::/48", ipv6_result))

    return set(ipv4_result) | set(ipv6_result)
