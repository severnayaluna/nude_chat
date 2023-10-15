from models import User

import asyncio

from aiogram import types

from typing import Optional, Any


def state_requiered(
    msg: types.Message,
    req_state: User.State,
    send_user: tuple[bool, Any] = (False, None),
    err_callback: Optional[callable] = None,
    *args,
    **kwargs):
    """Возвращает - True если юзер-стэйт слвпадает с запрошенным, иначе - False.

    Args:
        msg (types.Message): ... 
        req_state (User.State): ... 
        send_user (tuple[bool, Any], optional): ... . Defaults to (False, None).
        err_callback (Optional[callable], optional): ... . Defaults to None.

    Returns:
        _type_: _description_
    """    
    user, exists = User.get_or_create_by_msg(msg)
    if send_user[0]:
        send_user[1].user = user
        send_user[1].exists = not exists
    
    if user.state == req_state:
        return True
    else:
        if err_callback:
            loop = asyncio.get_event_loop()
            loop.create_task(err_callback(*args, **kwargs))
        return False