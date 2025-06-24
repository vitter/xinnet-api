# xinnet_dns/logger.py

import logging
import os

LOG_FILE = "cli_dns_log.txt"

os.makedirs(os.path.dirname(LOG_FILE) or ".", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def log_info(msg):
    logging.info(msg)

def log_error(msg):
    logging.error(msg)

def log_debug(msg):
    logging.debug(msg)

