from typing import Any

from aiogram import types

from .exceptions import *

from log import get_logger


logger: logging.Logger = get_logger(__name__)

def validate_msg(message: Any) -> None:
    """
    Проверяет, является ли переменная message классом aiogram.types.Message,
    если нет - возвращает исключение WrongType.
    """
    if not (mtype:=type(message)) is types.Message:
        raise WrongType(f'You must pass types.Message type, not {mtype}!', logging_level=logging.ERROR)
