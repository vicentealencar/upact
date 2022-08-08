from upact.cmdline.subcommands.ips.list_subcommand import ListAction
from upact.cmdline.subcommands.ips.block_subcommand import BlockAction


def sub_parser(subparsers):
    ips_subparser = subparsers.add_parser("ips")
    group = ips_subparser.add_mutually_exclusive_group()

    group.add_argument("--list", required=False, action=ListAction, nargs=0)
    group.add_argument("--block", nargs="+", dest="ips_to_block", action=BlockAction)

    return ips_subparser


