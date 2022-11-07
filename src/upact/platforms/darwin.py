import os
import subprocess

from upact.platforms.base_platform import BasePlatform

class Darwin(BasePlatform):
    
    def __init__(self, config):
        self.ips_to_block = set()
        self.config = config

    def update_permanently_blocked_ips(self, ips_to_block):
        self.ips_to_block.update([ip.address for ip in ips_to_block])
        self.update_firewall()

    def update_ips_from_urls(self, ips_to_block, ips_to_unblock):
        self.ips_to_block.update([ip.address for ip in ips_to_block])
        self.update_firewall()

    def update_firewall(self):
        ip_addresses = self.ips_to_block

        with open(self.config.PF_CONF_TEMPLATE, "r") as etc_pf:
            pf_conf = etc_pf.read()

        with open(self.config.BLOCKED_IPS_FILE, "w") as blocked_ips_file:
            blocked_ips_file.write("\n".join(ip_addresses))

        pf_conf += 'table <blocked_ips> persist file "{0}"'.format(os.path.join(os.getcwd(), self.config.BLOCKED_IPS_FILE))
        pf_conf += "\n"

        pf_conf += "block return from any to <blocked_ips>"
        pf_conf += "\n"

        with open(self.config.PF_CONF_PATH, "w+") as pf_conf_file:
            pf_conf_file.write(pf_conf)

        subprocess.call(["sudo", "pfctl", "-E", "-f", self.config.PF_CONF_PATH])
