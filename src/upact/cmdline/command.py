import argparse
import config

import peewee as pw

from upact.cmdline.subcommands import urls
from upact.cmdline.subcommands import ips
from upact.models import database_proxy

def run():
    db = pw.SqliteDatabase(config.DATABASE_FILE)
    db.connect()
    database_proxy.initialize(db)

    main_parser = argparse.ArgumentParser()
    subparsers = main_parser.add_subparsers()

    urls.sub_parser(subparsers)
    ips.sub_parser(subparsers)

    parsed_args = main_parser.parse_args()

    if getattr(parsed_args, 'init_command', None):
        parsed_args.init_command(parsed_args)()
