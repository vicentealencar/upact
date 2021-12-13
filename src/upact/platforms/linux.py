import subprocess
import logging

class Linux:
    def update_firewall(self, ips_to_block, ips_to_unblock, config):
        command = {
                4: "iptables",
                6: "ip6tables"
            }

        for ip in ips_to_block:
            full_command = ["sudo", command[ip.version], "-A", "OUTPUT", "-d", ip.address, "-j", "DROP"]
            logging.info(f'Running {" ".join(full_command)}')
            subprocess.call(full_command)

        for ip in ips_to_unblock:
            full_command = ["sudo", command[ip.version], "-D", "OUTPUT", "-d", ip.address, "-j", "DROP"]
            logging.info(f'Running {" ".join(full_command)}')
            subprocess.call(full_command)
