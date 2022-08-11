import logging

import peewee as pw

from upact.models import database_proxy

def init_db(database_file):

    logging.info("Initializing db")

    db = pw.SqliteDatabase(database_file)
    logging.info(f"Connecting to database at {database_file}")
    db.connect()
    database_proxy.initialize(db)
    logging.info("Connection successful")

    return db
