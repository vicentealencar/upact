import json
import os
import socket

from datetime import datetime
from dateutil import rrule
from dateutil.parser import parse
from recurrent import RecurringEvent

def is_day_in_recurrence(recurrence_string, day):
    recurrence = rrule.rrulestr(RecurringEvent().parse(recurrence_string))
    return (recurrence[0] - day).days == 0

def is_time_in_interval(begin_str, end_str, time):
    begin_time = parse(begin_str).time()
    end_time = parse(begin_str).time()

    return begin_time <= time and time <= end_time

with open("/etc/pf.conf", "r") as etc_pf:
    pf_conf = etc_pf.read()

with open("./block_list.txt", "r") as block_list_file:
    block_list = [s.strip() for s in block_list_file.readlines()]

with open("./exceptions.json") as exceptions_file:
    block_exceptions = json.loads(exceptions_file.read())

for be in block_exceptions:
    today = datetime.now()

    if not is_day_in_recurrence(be["frequency"], today):
        continue

    if reduce(operator.and_, 
            map(lambda period: is_time_in_interval(period[0], period[1], today.time()), be['time_periods'])):

        block_list = list(set(block_list) - set(be['urls']))

# TODO: test code above



ips_to_block = []
for host_name in block_list:
    ignore_me, ignore_me, ip_addresses = socket.gethostbyname_ex(host_name)
    ips_to_block += ip_addresses

for ip in ips_to_block:
    pf_conf += "block return from any to %s" % ip
    pf_conf += "\n"

file_name = "./pf_conf.conf"
with open(file_name, "w") as pf_conf_file:
    pf_conf_file.write(pf_conf)

# TODO: Use recurrent to parse interval string and dateutil to check if current date/time matches that interval

#os.remove(file_name)
