import argparse
from recurrent import RecurringEvent

from upact.cmdline.subcommands.urls.block_subcommand import BlockSubcommand

class BlockAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, 'command', BlockSubcommand)
        setattr(namespace, self.dest, values)

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


def dispatch(namespace):
    kwargs = vars(namespace)
    command_class = kwargs.pop('command', None)
    command_object = command_class(**{k: kwargs[k] for k in command_class.kwargs() if k in kwargs})

    command_object()
    

def sub_parser(subparsers):
    block_sites = subparsers.add_parser("urls")
    group = block_sites.add_mutually_exclusive_group()

    group.add_argument("--block", nargs="+", dest="urls_to_block", action=BlockAction)
    group.add_argument("--remove", nargs="+", required=False, dest="urls_to_remove")
    group.add_argument("--list", required=False, action="store_true")
    block_sites.add_argument("--allow", nargs=1, required=False, action=AllowAction, dest="playtime_days")
    block_sites.add_argument("--at-interval", nargs="+", required=False, action=AtIntervalAction, dest="playtime_hours")

    block_sites.set_defaults(func=dispatch)

    return block_sites

