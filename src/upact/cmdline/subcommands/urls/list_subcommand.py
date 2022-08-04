import argparse

from texttable import Texttable

from upact import store
from upact.models import Uri


class ListSubcommand(object):

    def __init__(self):
        self.result = None

    def _render(self):
        table = Texttable()

        table.add_row(["Blocked Url", "Exceptions"])

        for uri in self.result:
            url_name = uri.name
            table.add_row(
                [uri.name,
                "\n".join([f"{pt.frequency} from {pt.from_time} to {pt.to_time}" for pt in (uri.playtime_rules or [])])])

        table.set_cols_align(["l", "c"])
        table.set_cols_valign(["m", "m"])
        self.display_string = table.draw()
        print(self.display_string)

    def __call__(self):
        self.result = store.uri.list(Uri.TYPE_URL)
        self._render()


class ListAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace,
                'init_command',
                lambda namespace: ListSubcommand())

