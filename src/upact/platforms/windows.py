import subprocess
import logging


from upact.platforms.base_platform import BasePlatform
import upact.fences.web as web_fence

class Windows(BasePlatform):

    def _write(self, stream, blob_str):
        logging.info(blob_str)
        stream.write(bytes(blob_str, 'utf-8'))

    def block_ips(self, ip_addresses, rule_name):
        with subprocess.Popen("powershell.exe", stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as process:
            self._write(process.stdin, "$ips_to_block = @()\n")
            for ip in ip_addresses:
                self._write(process.stdin, f'$ips_to_block += "{ip.address}"\n')

            self._write(process.stdin, f'New-NetFirewallRule -DisplayName "{rule_name}" -Direction Outbound -Action Block -RemoteAddress $ips_to_block\n')
            process.stdin.flush()


    def _remove_rule(self, rule_name):
        remove_rule_command = f'netsh advfirewall firewall delete rule name="{rule_name}"'
        logging.info(remove_rule_command)
        subprocess.call(remove_rule_command)

    def create_firewall_rule(self, ips_to_block, rule_name="upact blocked ips"):

        logging.info("Removing existing rules...")
        self._remove_rule(rule_name)

        if ips_to_block:
            logging.info("Adding new rules...")
            self.block_ips(ips_to_block, rule_name)

        logging.info("Done updating blocked ips")

    def update_permanently_blocked_ips(self, ips_to_block):
        logging.info("Updating permanently blocked ips")

        self.create_firewall_rule(ips_to_block=ips_to_block, rule_name="upact permanently blocked ips")

        logging.info("Update successful")

    def update_ips_from_urls(self, ips_to_block, ips_to_unblock):
        logging.info("Updating ips from blocked Urls")

        self.create_firewall_rule(ips_to_block, rule_name="upact ips from urls")

        logging.info("Update successful")
