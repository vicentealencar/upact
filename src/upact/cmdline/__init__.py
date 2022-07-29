import argparse

from upact.cmdline.subcommands import urls

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers()

urls.sub_parser(subparsers)

