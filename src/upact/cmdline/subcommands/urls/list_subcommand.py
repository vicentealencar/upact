import argparse


class ListSubcommand(object):

    def __init__(self):
        self.result = None

    def _render(self):
        print("hello list!!")

    def __call__(self):
        self._render()


class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace,
                'command',
                lambda namespace: ListSubcommand()())

