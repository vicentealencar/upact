import argparse
import ulysses.store.staging as staging

from ulysses.models import BlockedSites
from recurrent import RecurringEvent


class PlaytimeDaysAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if namespace.add is None:
            raise argparse.ArgumentError(self, 'This argument must be provided along with --add. E.g.: --add facebook.com --playtime_days="every weekend"')

        if len(values) != 1:
            raise argparse.ArgumentError(self, 'This argument must be provided only once and contain a single recurrence string. E.g.: --playtime_days="every weekend"')

        play_days = values[0]

        if RecurringEvent().parse(play_days) is None:
            raise argparse.ArgumentError(self, "Invalid recurrence input %s" % play_days)

        if getattr(namespace, self.dest) is not None:
            raise argparse.ArgumentError(self, "--playtime_days can only be provided once")

        setattr(namespace, self.dest, play_days)


class PlaytimeHoursAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if namespace.playtime_days is None:
            raise argparse.ArgumentError(self, 'This argument must be provided along with --playtime_days. E.g.: --add facebook.com --playtime_days="every weekend" --playtime_hours 19:00 20:00')

        if len(values) != 2:
            raise argparse.ArgumentError(self, "Must contain a range of hours, e.g.: --playtime_hours 19:00 20:00")

        if getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])

        getattr(namespace, self.dest).append(values)


class RemoveAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if namespace.add is not None or namespace.playtime_hours is not None or namespace.playtime_days is not None:
            raise argparse.ArgumentError(self, 'This argument cannot be specified with any other parameter')

        setattr(namespace, self.dest, values)


def command(parameters, store):
    if parameters.add:
        sites_to_block = BlockedSites(parameters.add, parameters.playtime_days, parameters.playtime_hours)
        blocked_sites_staging = store()
        blocked_sites_staging.add(sites_to_block)


def sub_parser(subparsers, store=staging.BlockedSites):
    block_sites = subparsers.add_parser("block-sites")
    block_sites.add_argument("--add", nargs="+")
    block_sites.add_argument("--playtime_days", nargs=1, required=False, action=PlaytimeDaysAction)
    block_sites.add_argument("--playtime_hours", nargs="+", required=False, action=PlaytimeHoursAction)
    block_sites.add_argument("--remove", nargs="+", required=False, action=RemoveAction)
    block_sites.set_defaults(func=lambda x: command(x, store))

    return block_sites
