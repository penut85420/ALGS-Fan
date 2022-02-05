import json
import pickle
import sys

from loguru import logger


def load_json(fp):
    with open(fp, "r", encoding="UTF-8") as f:
        return json.load(f)


def load_token(token):
    creds = bytearray.fromhex(token)
    return pickle.loads(creds)


def set_logger(log_path="Logs/algs.log"):
    log_format = (
        "{time:YYYY-MM-DD HH:mm:ss.SSSSSS} | "
        "<lvl>{level: ^9}</lvl> | "
        "{message}"
    )
    logger.add(sys.stderr, level="INFO", format=log_format)
    logger.add(
        log_path,
        rotation="1 day",
        retention="7 days",
        level="INFO",
        encoding="UTF-8",
        compression="gz",
        format=log_format,
    )
