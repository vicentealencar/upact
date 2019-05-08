import os
import socket

with open("/etc/pf.conf", "r") as etc_pf:
    pf_conf = etc_pf.read()

with open("./block_list.txt", "r") as block_list_file:
    block_list = [s.strip() for s in block_list_file.readlines()]

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
