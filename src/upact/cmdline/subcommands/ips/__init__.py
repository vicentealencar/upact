from upact.cmdline.subcommands.ips.list_subcommand import ListAction


def sub_parser(subparsers):
    ips_subparser = subparsers.add_parser("ips")
    ips_subparser.add_argument("--list", required=False, action=ListAction, nargs=0)

    return ips_subparser


