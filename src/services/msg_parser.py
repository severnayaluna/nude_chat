from aiogram import types

from log import get_logger

from .exceptions import *
from services.validator import validate_msg


logger = get_logger(__name__)

def parse_content(message: types.Message):
    validate_msg(message)

    ctype = str(message.content_type)
    foo_name = f'send_{ctype}'

    if ctype == 'text':
        return message.text, 'send_message'

    unparsed_content = getattr(message, str(ctype))

    if type(unparsed_content) is not list:
        unparsed_content = [unparsed_content]

    return unparsed_content[-1]['file_id'], foo_name
