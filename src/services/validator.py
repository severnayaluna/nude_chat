from typing import Any
from aiogram import types

from .exceptions import *

from log import get_logger


logger = get_logger(__name__)

def validate_msg(message: Any):
    if not (mtype:=type(message)) is types.Message:
        raise WrongType(f'You must pass types.Message type, not {mtype}!')
