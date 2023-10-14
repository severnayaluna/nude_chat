from models import User

import asyncio

from aiogram import types

from typing import Optional


def state_requiered(
    msg: types.Message,
    req_state: User.State,
    err_callback: Optional[callable] = None,
    *args,
    **kwargs):
    if User.get_or_create_by_msg(msg)[0].state == req_state:
        return True
    else:
        if err_callback:
            loop = asyncio.get_event_loop()
            loop.create_task(err_callback(*args, **kwargs))
        return False