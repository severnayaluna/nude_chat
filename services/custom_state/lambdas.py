from models import User

import asyncio

from aiogram import types

from typing import Optional, Any


def state_requiered(
    msg: types.Message,
    state_filter: dict,
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
    user: User
    if send_user[0]:
        send_user[1].user = user
        send_user[1].exists = not exists
    
    for state_name in state_filter:
        acess = state_filter[state_name].is_state_acessed(user.get_state(state_name))
        if not acess:
            if err_callback:
                loop = asyncio.get_event_loop()
                loop.create_task(err_callback(*args, **kwargs))
            return False
    
    return True
