import subprocess
import logging

class Windows:
    # TODO: 1. Get all rules
    #       2. Filter the ones created by upact. Use the following powershell script: (New-object -comObject HNetCfg.FwPolicy2).rules | select name | findstr /i "Cortana"
    #       3. unblock them

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
        try:
            return subprocess.check_output(["powershell.exe", 
                                            "-Command",
                                            f"(New-object -comObject HNetCfg.FwPolicy2).rules | select name | findstr /i '{rule_prefix}'"], 
                                        shell=True)
        except subprocess.CalledProcessError as ex:
            return b''

    def _parse_firewall_rules(self, raw_output):
        return [s.strip() for s in raw_output.decode('utf-8').strip().split("\r\n") if s]

    def _list_firewall_rules_names(self):
        return self._parse_firewall_rules(self._raw_firewall_rules_output(self.RULE_NAME_PREFIX))

    def update_firewall(self, ips_to_block, ips_to_unblock, config):

        for rule_name in self._list_firewall_rules_names():
            self._remove_rule(rule_name)

        for ip in ips_to_block:
            self._block_ip(ip.address)
