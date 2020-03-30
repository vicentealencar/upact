import argparse

from . import blocked_sites

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers()

blocked_sites.sub_parser(subparsers)
