import argparse
from recurrent import RecurringEvent

class PlaytimeHoursAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) != 2:
            raise argparse.ArgumentError(self, "Must contain a range of hours, e.g.: --playtime_hours 19:00 20:00")

        if getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])

        getattr(namespace, self.dest).append(values)


class PlaytimeDaysAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if len(values) != 1:
            raise argparse.ArgumentError(self, 'This argument must be provided only once and contain a single recurrence string. E.g.: --playtime_days="every weekend"')

        play_days = values[0]

        if RecurringEvent().parse(play_days) is None:
            raise argparse.ArgumentError(self, "Invalid recurrence input %s" % play_days)

        if getattr(namespace, self.dest) is not None:
            raise argparse.ArgumentError(self, "--playtime_days can only be provided once")


        setattr(namespace, self.dest, play_days)


def sub_parser(subparsers):
    block_sites = subparsers.add_parser("block-sites")
    block_sites.add_argument("--add", nargs="+", required=True)
    block_sites.add_argument("--playtime_days", nargs=1, required=False, action=PlaytimeDaysAction)
    block_sites.add_argument("--playtime_hours", nargs="+", required=False, action=PlaytimeHoursAction)

    return block_sites
