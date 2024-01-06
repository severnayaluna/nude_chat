import os
from typing import Any

import dotenv

from log import get_logger


logger = get_logger(__name__)


def load(name: str, rs: bool = False) -> Any:
    var = os.getenv(name)
    if not var:
        logger.error(f'{name} was not founded in .env file!')
        if rs: raise AttributeError(f'{name} was not founded in .env file!')
        return None
    return var


def raise_env_error():
    logger.error(f'.env file was not loaded!')
    raise AttributeError(f'.env file was not loaded!')


dotenv.load_dotenv(os.path.join(os.getcwd(), '.env')) or raise_env_error()
logger.info('.env file was loaded successfully')


BOT_TOKEN = load('BOT_TOKEN', True)

REDIS_HOST = load('REDIS_HOST', True)
REDIS_PORT = load('REDIS_PORT', True)
