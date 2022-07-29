import argparse

from upact.cmdline.subcommands.urls.block_subcommand import BlockSubcommand, BlockAction, AllowAction, AtIntervalAction


def sub_parser(subparsers):
    urls_subparser = subparsers.add_parser("urls")
    group = urls_subparser.add_mutually_exclusive_group()

    group.add_argument("--block", nargs="+", dest="urls_to_block", action=BlockAction)
    group.add_argument("--remove", nargs="+", required=False, dest="urls_to_remove")
    group.add_argument("--list", required=False, action="store_true")
    urls_subparser.add_argument("--allow", nargs=1, required=False, action=AllowAction, dest="playtime_days")
    urls_subparser.add_argument("--at-interval", nargs="+", required=False, action=AtIntervalAction, dest="playtime_hours")

    return urls_subparser

