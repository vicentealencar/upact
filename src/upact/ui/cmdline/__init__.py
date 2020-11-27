import argparse

from . import block_sites

main_parser = argparse.ArgumentParser()
subparsers = main_parser.add_subparsers()

block_sites.sub_parser(subparsers)
