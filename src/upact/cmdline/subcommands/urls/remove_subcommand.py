import argparse


class RemoveSubcommand(object):

    def __init__(self, urls_to_remove):
        self.urls_to_remove = urls_to_remove
        self.result = None

    def _render(self):
        print("hello remove!!")

    def __call__(self):
        self._render()


class RemoveAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

        setattr(namespace,
                'init_command',
                lambda namespace: RemoveSubcommand(namespace.urls_to_remove))
