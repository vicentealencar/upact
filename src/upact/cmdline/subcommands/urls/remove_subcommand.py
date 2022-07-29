import argparse

from upact import store
from upact.models import Uri


class RemoveSubcommand(object):

    def __init__(self, urls_to_remove):
        self.urls_to_remove = urls_to_remove
        self.result = None

    def _render(self):
        print("Success")

    def __call__(self):
        self.result = store.uri.remove(self.urls_to_remove)
        self._render()


class RemoveAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

        setattr(namespace,
                'init_command',
                lambda namespace: RemoveSubcommand(namespace.urls_to_remove))
