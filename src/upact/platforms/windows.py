import subprocess
import logging

class Windows:

    RULE_NAME_PREFIX = "upact"

    def _rule_name(self, ip):
        return f"{self.RULE_NAME_PREFIX} {ip}"

    def _block_ip(self, ip):
        add_rule_command = f'netsh advfirewall firewall add rule name="{self._rule_name(ip)}" dir=out action=block remoteip={ip}'
        logging.info(add_rule_command)
        subprocess.call(add_rule_command)

    def _remove_rule(self, rule_name):
        remove_rule_command = f'netsh advfirewall firewall delete rule name="{rule_name}"'
        logging.info(remove_rule_command)
        subprocess.call(remove_rule_command)

    def _raw_firewall_rules_output(self, rule_prefix):
        command = f"(New-object -comObject HNetCfg.FwPolicy2).rules | select name | findstr /i '{rule_prefix}'"
        try:
            logging.info(f"Running powershell command {command}")
            return subprocess.check_output(["powershell.exe", 
                                            "-Command",
                                            command], 
                                        shell=True)
        except subprocess.CalledProcessError as ex:
            logging.info(f"Exception from powershell command {command}")
            return b''

    def _parse_firewall_rules(self, raw_output):
        return [s.strip() for s in raw_output.decode('utf-8').strip().split("\r\n") if s]

    def _list_firewall_rules_names(self):
        return self._parse_firewall_rules(self._raw_firewall_rules_output(self.RULE_NAME_PREFIX))

    def update_firewall(self, ips_to_block, ips_to_unblock, config):

        logging.info("Removing existing rules...")
        for rule_name in self._list_firewall_rules_names():
            self._remove_rule(rule_name)

        logging.info("Adding new rules...")
        for ip in ips_to_block:
            self._block_ip(ip.address)

        logging.info("Done updating blocked ips")
