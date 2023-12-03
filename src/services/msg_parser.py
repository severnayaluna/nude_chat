from typing import Union

from aiogram import types

from log import get_logger

from .exceptions import *

from services.validator import validate_msg


logger: logging.Logger = get_logger(__name__)


def parse_content(message: types.Message) -> tuple[str, str]:
    """
    Парсит aiogram-класс сообщения. Ищет медиа.
    Возвращает айди-медиа и имя функции которую надо вызвать чтобы отправить это медиа.
    """
    validate_msg(message)

    ctype: str = str(message.content_type)
    foo_name: str = f'send_{ctype}'

    if ctype == 'text':
        return message.text, 'send_message'

    unparsed_content = getattr(message, str(ctype))

    if type(unparsed_content) is not list:
        unparsed_content = [unparsed_content]

    return unparsed_content[-1]['file_id'], foo_name
