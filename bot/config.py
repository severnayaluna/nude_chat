import os

from typing import Any, Literal

import dotenv

from .log import get_logger


logger = get_logger(__name__)


def load(name: str, rs: bool = False, mode = Literal['test', 'prod']) -> Any:
    name = f'{name}_{mode}'.upper()
    logger.info('Loading .env/%s', name)
    var = os.getenv(name)

    if not var:
        logger.error(f'{name} was not founded in .env file!')
        if rs: raise AttributeError(f'{name} was not founded in .env file!')
        return None
    return var


def raise_env_error():
    logger.error(f'.env file was not loaded!')
    raise AttributeError(f'.env file was not loaded!')



class Config:
    def load_env(self) -> None:
        dotenv.load_dotenv(os.path.join(os.getcwd(), '.env')) or raise_env_error()
        logger.info('.env file was loaded successfully')

    def __init__(self, mode=Literal['test', 'prod']) -> None:
        self.load_env()
        self.BOT_TOKEN = load('BOT_TOKEN', True, mode)

        self.REDIS_HOST = load('REDIS_HOST', True, mode)
        self.REDIS_PORT = load('REDIS_PORT', True, mode)
