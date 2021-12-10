import os

DATA_FOLDER = "./data"
STATIC_FOLDER = os.path.join(DATA_FOLDER, "static")
DATABASE_FILE = os.path.join(DATA_FOLDER, "database.db")
AUTO_GENERATED_FOLDER = os.path.join(DATA_FOLDER, "auto_generated")

IP_EXPIRY_TIME = 24 # how many hours to keep dangling ips around

# Static
PF_CONF_TEMPLATE = os.path.join(STATIC_FOLDER, "conf_template.conf")

# Auto generated files
PF_CONF_PATH = os.path.join(AUTO_GENERATED_FOLDER, "pf.conf")
BLOCKED_IPS_FILE = os.path.join(AUTO_GENERATED_FOLDER, "blocked_ips.txt")
