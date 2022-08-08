import argparse

from collections import defaultdict
from texttable import Texttable

from upact import store
import upact.store.ips


class ListSubcommand(object):

    def __init__(self):
        self.result = None

    def _render(self):
        table = Texttable()

        table.add_row(["Url", "Ips"])

        uri_ip_table = defaultdict(list)
        for ip in self.result:
            uri_ip_table[ip.uri.name].append(ip.address)

        for (uri_name, ip_addresses) in uri_ip_table.items():
            table.add_row(
                [uri_name,
                "\n".join(ip_addresses)])

        table.set_cols_align(["l", "c"])
        table.set_cols_valign(["m", "m"])
        self.display_string = table.draw()
        print(self.display_string)

    def __call__(self):
        self.result = store.ips.list()
        self._render()


class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace,
                'init_command',
                lambda namespace: ListSubcommand())

