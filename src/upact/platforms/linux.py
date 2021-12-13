import subprocess

class Linux:
    def update_firewall(self, ips_to_block, ips_to_unblock, config):
        command = {
                4: "iptables",
                6: "ip6tables"
            }

        for ip in ips_to_block:
            subprocess.call(["sudo", command[ip.version], "-A", "OUTPUT", "-d", ip.address, "-j", "DROP"])

        for ip in ips_to_unblock:
            subprocess.call(["sudo", command[ip.version], "-D", "OUTPUT", "-d", ip.address, "-j", "DROP"])
