from upact.cmdline.subcommands.urls.block_subcommand import BlockAction, AllowAction, AtIntervalAction
from upact.cmdline.subcommands.urls.remove_subcommand import RemoveAction
from upact.cmdline.subcommands.urls.list_subcommand import ListAction


def sub_parser(subparsers):
    urls_subparser = subparsers.add_parser("urls")
    group = urls_subparser.add_mutually_exclusive_group()

    group.add_argument("--block", nargs="+", dest="urls_to_block", action=BlockAction)
    group.add_argument("--remove", nargs="+", required=False, dest="urls_to_remove", action=RemoveAction)
    group.add_argument("--list", required=False, action=ListAction, nargs=0)
    urls_subparser.add_argument("--allow", nargs=1, required=False, action=AllowAction, dest="playtime_days")
    urls_subparser.add_argument("--at-interval", nargs="+", required=False, action=AtIntervalAction, dest="playtime_hours")

    return urls_subparser

