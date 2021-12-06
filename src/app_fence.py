import subprocess
import logging
import config

import peewee as pw

from upact.models import *


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info("Running upact app")

    db = pw.SqliteDatabase(config.DATABASE_FILE)
    db.connect()
    database_proxy.initialize(db)

    apps_to_block = [uri.name for uri in Uri.select().where(Uri.type_uri == 'application') if not(any([playtime.is_active() for playtime in uri.playtime_rules]))]

    for app_to_kill in apps_to_block:
        logging.info(f"Killing {app_to_kill}")
        subprocess.call(["sudo", "pkill", "-9", app_to_kill])
