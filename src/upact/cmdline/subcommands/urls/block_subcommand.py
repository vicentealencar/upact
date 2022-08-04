import argparse
from recurrent import RecurringEvent

from upact import store
from upact.models import Uri


class BlockSubcommand(object):

    def __init__(self, urls_to_block, playtime_days, playtime_hours):
        self.urls_to_block = urls_to_block
        self.playtime_days = playtime_days
        self.playtime_hours = playtime_hours
        self.result = None

    def _render(self):
        print("Success")

    def __call__(self):
        self.result = store.uri.block(self.urls_to_block, self.playtime_days, self.playtime_hours)
        self._render()


class BlockAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

        setattr(namespace,
                'init_command',
                lambda namespace: BlockSubcommand(namespace.urls_to_block, namespace.playtime_days, namespace.playtime_hours))


class AllowAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if namespace.urls_to_block is None:
            raise argparse.ArgumentError(self, 'This argument must be provided along with --block. E.g.: --block facebook.com --allow "every weekend"')

        if len(values) != 1:
            raise argparse.ArgumentError(self, 'This argument must be provided only once and contain a single recurrence string. E.g.: --allow="every weekend"')

        play_days = values[0]

        if RecurringEvent().parse(play_days) is None:
            raise argparse.ArgumentError(self, "Invalid recurrence input %s" % play_days)

        if getattr(namespace, self.dest) is not None:
            raise argparse.ArgumentError(self, "--allow can only be provided once")

        setattr(namespace, self.dest, play_days)


class AtIntervalAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if namespace.playtime_days is None:
            raise argparse.ArgumentError(self, 'This argument must be provided along with --allow. E.g.: --block facebook.com --allow="every weekend" --at_interval 19:00 20:00')

        if len(values) != 2:
            raise argparse.ArgumentError(self, "Must contain a range of hours, e.g.: --at_interval 19:00 20:00")

        if getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])

        getattr(namespace, self.dest).append(values)
