import os

from typing import Any, Literal

import dotenv

from .log import get_logger


logger = get_logger(__name__)


def load(name: str, path: str, rs: bool = False) -> Any:
    logger.info('Loading %s:%s', path, name)
    var = os.getenv(name)

    if not var:
        logger.error('%s was not founded in %s file!', name, path)
        if rs: raise AttributeError('%s was not founded in %s file!' % (name, path))
        return None
    return var


def raise_env_error(path: str):
    logger.error('%s file was not loaded!', path)
    raise AttributeError('%s file was not loaded!' % (path,))



class Config:
    def load_env(self, path: str) -> None:
        dotenv.load_dotenv(os.path.join(os.getcwd(), path)) or raise_env_error(path)
        logger.info('%s file was loaded successfully', path)

    def __init__(self, path: str) -> None:
        self.load_env(path)

        self.BOT_TOKEN = load('BOT_TOKEN', path, True)

        self.REDIS_HOST = load('REDIS_HOST', path, True)
        self.REDIS_PORT = load('REDIS_PORT', path, True)
