import json
import operator
import subprocess
import logging

import config

from upact.datetime import is_time_in_interval, is_day_in_recurrence

from datetime import datetime
from functools import reduce


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


logging.info("Running upact app")

with open(config.APPS_TO_BLOCK, "r") as block_list_file:
    block_list = [s.strip() for s in block_list_file.readlines()]

with open(config.APP_PLAYTIME_RULES) as exceptions_file:
    block_exceptions = json.loads(exceptions_file.read())

for be in block_exceptions:
    today = datetime.now()

    if not is_day_in_recurrence(be["frequency"], today):
        continue

    if reduce(operator.or_, 
            map(lambda period: is_time_in_interval(period[0], period[1], today.time()), be['time_periods'])):

        print("The APP(s) %s are currently accessible. Rule: %s" % (be['apps'], be))

        block_list = list(set(block_list) - set(be['apps']))

for app_to_kill in block_list:
    logging.info(f"Killing {app_to_kill}")
    subprocess.call(["sudo", "pkill", "-9", app_to_kill])
