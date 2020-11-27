import dns.resolver
import json
import operator
import os
import requests
import socket
import subprocess

import config
import networking

from datetime import datetime
from dateutil import rrule
from dateutil.parser import parse
from functools import reduce
from recurrent import RecurringEvent

try:
    with open(config.ALL_DNSES_FILE, "w") as file_dns_all:
        file_dns_all.write(requests.get(config.ALL_DNSES_URL).content.decode("utf-8"))
except:
    print("DNS file could not be downloaded from: %s" % config.ALL_DNSES_URL)

with open(config.ALL_DNSES_FILE, "r") as file_dns_all:
    all_dnses = set([line.strip() for line in file_dns_all.readlines()])

with open(config.ALLOWED_DNSES_FILE) as dns_allowed:
    allowed_dnses = set([addr.strip() for addr in dns_allowed.readlines()])

dnses_to_block = all_dnses - allowed_dnses

with open(config.PF_CONF_TEMPLATE, "r") as etc_pf:
    pf_conf = etc_pf.read()

with open(config.URLS_TO_BLOCK, "r") as block_list_file:
    block_list = [s.strip() for s in block_list_file.readlines()]

with open(config.PORTS_TO_BLOCK, "r") as block_ports_file:
    ports_to_block = [int(s) for s in block_ports_file.readlines()]

with open(config.WEB_PLAYTIME_RULES) as exceptions_file:
    block_exceptions = json.loads(exceptions_file.read())

for be in block_exceptions:
    today = datetime.now()

    if not is_day_in_recurrence(be["frequency"], today):
        continue

    if reduce(operator.or_, 
            map(lambda period: is_time_in_interval(period[0], period[1], today.time()), be['time_periods'])):

        print("The URL(s) %s are currently accessible" % be['urls'])

        block_list = list(set(block_list) - set(be['urls']))


# we will nslookup google to check if we have internet connection
try:
    networking.dns_lookup(config.INTERNET_CONNECTIVITY_URL)
except socket.gaierror as ex:
    print("Couldn't lookup %s. Aborting." % config.INTERNET_CONNECTIVITY_URL)
    exit(0)

ips_to_block = set()
for host_name in block_list:
    try:
        ip_addresses = networking.dns_lookup(host_name)
        ips_to_block.update(ip_addresses)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN) as ex:
        print(ex.msg)

ips_to_block.update(dnses_to_block)

with open(config.BLOCKED_IPS_FILE, "w") as blocked_ips_file:
    blocked_ips_file.write("\n".join(ips_to_block))

pf_conf += 'table <blocked_ips> persist file "{0}"'.format(os.path.join(os.getcwd(), config.BLOCKED_IPS_FILE))
pf_conf += "\n"

pf_conf += "block return from any to <blocked_ips>"
pf_conf += "\n"

for port in ports_to_block:
    pf_conf += "block return inet proto { tcp, udp } from any to any port %s" % port
    pf_conf += "\n"


with open(config.PF_CONF_PATH, "w+") as pf_conf_file:
    pf_conf_file.write(pf_conf)


subprocess.call(["sudo", "pfctl", "-E", "-f", config.PF_CONF_PATH])
