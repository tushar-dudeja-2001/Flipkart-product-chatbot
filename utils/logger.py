import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)
LOG_FILE = f"logs/log_{datetime.now():%Y-%m-%d}.log"

logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_logger(name):
    return logging.getLogger(name)
