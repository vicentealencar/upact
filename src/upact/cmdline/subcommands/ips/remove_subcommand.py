import argparse

from upact import store
import upact.store.ips


class RemoveSubcommand(object):

    def __init__(self, ips_to_remove):
        self.ips_to_remove = ips_to_remove
        self.result = None

    def _render(self):
        print("Success")

    def __call__(self):
        self.result = store.ips.remove(self.ips_to_remove)
        self._render()


class RemoveAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

        setattr(namespace,
                'init_command',
                lambda namespace: RemoveSubcommand(namespace.ips_to_remove))

