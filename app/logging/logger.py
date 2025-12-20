import logging
from python_json_logger import json_logger

def setup_logging():
    logger = logging.getLogger("movie_rating")
    logger.setLevel(logging.INFO)

    formatter = json_logger.JsonFormatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(funcName)s)'
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

logger = setup_logging()
