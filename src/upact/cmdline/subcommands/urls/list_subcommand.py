import argparse

from upact import store
from upact.models import Uri


class ListSubcommand(object):

    def __init__(self):
        self.result = None

    def _render(self):
        for uri in self.result:
            print(f"Url: {uri.name}")

    def __call__(self):
        self.result = store.uri.list(Uri.TYPE_URL)
        self._render()


class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace,
                'init_command',
                lambda namespace: ListSubcommand())

