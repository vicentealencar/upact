import os

DATA_FOLDER = "./data"
CONFIG_FOLDER = os.path.join(DATA_FOLDER, "private")
STATIC_FOLDER = os.path.join(DATA_FOLDER, "static")
DATABASE_FILE = os.path.join(DATA_FOLDER, "database.db")
AUTO_GENERATED_FOLDER = os.path.join(DATA_FOLDER, "auto_generated")

# Configuratios
ALLOWED_DNSES_FILE = os.path.join(CONFIG_FOLDER, "nameservers-allowed.txt")
URLS_TO_BLOCK = os.path.join(CONFIG_FOLDER, "url_block_list.txt")
PORTS_TO_BLOCK = os.path.join(CONFIG_FOLDER, "block_ports.txt")
WEB_PLAYTIME_RULES = os.path.join(CONFIG_FOLDER, "web_playtime_rules.json")

APPS_TO_BLOCK = os.path.join(CONFIG_FOLDER, "app_block_list.txt")
APP_PLAYTIME_RULES = os.path.join(CONFIG_FOLDER, "app_playtime_rules.json")

# Static
PF_CONF_TEMPLATE = os.path.join(STATIC_FOLDER, "conf_template.conf")

# URLS
ALL_DNSES_URL = "https://public-dns.info/nameservers.txt"
INTERNET_CONNECTIVITY_URL = "www.google.com"

# Auto generated files
ALL_DNSES_FILE = os.path.join(AUTO_GENERATED_FOLDER, "nameservers-all.txt")
PF_CONF_PATH = os.path.join(AUTO_GENERATED_FOLDER, "pf.conf")
STAGING_URLS_TO_BLOCK = os.path.join(AUTO_GENERATED_FOLDER, "staging_urls_to_block.jsonl")
BLOCKED_IPS_FILE = os.path.join(AUTO_GENERATED_FOLDER, "blocked_ips.txt")
BLOCKED_IPS_JSON = os.path.join(AUTO_GENERATED_FOLDER, "blocked_ips.json")
