import os

FOLDER = "./sample"
ALL_DNSES_URL = "https://public-dns.info/nameservers.txt"
ALL_DNSES_FILE = os.path.join(FOLDER, "nameservers-all.txt")
ALLOWED_DNSES_FILE = os.path.join(FOLDER, "nameservers-allowed.txt")
PF_CONF_PATH = os.path.join(FOLDER, "pf.conf")
PF_CONF_TEMPLATE = os.path.join(FOLDER, "conf_template.conf")
INTERNET_CONNECTIVITY_URL = "www.google.com"
URLS_TO_BLOCK = os.path.join(FOLDER, "block_list.txt")
PORTS_TO_BLOCK = os.path.join(FOLDER, "block_ports.txt")
PLAYTIME_RULES = os.path.join(FOLDER, "playtime_rules.json")
