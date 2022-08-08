import argparse
import upact.store.ips

from upact import store
from upact.models import Uri


class BlockSubcommand(object):

    def __init__(self, ips_to_block):
        self.ips_to_block = ips_to_block
        self.result = None

    def _render(self):
        print("Success")

    def __call__(self):
        self.result = store.ips.block(self.ips_to_block, uri=Uri.permanently_blocked_ips_uri())
        self._render()


class BlockAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

        setattr(namespace,
                'init_command',
                lambda namespace: BlockSubcommand(namespace.ips_to_block))
