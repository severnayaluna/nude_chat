from models import User
from .custom_state.lambdas import state_requiered

from typing import Any, Optional


def my_msg_handler(
    dispatcher,
    commands = None,
    regexp = None,
    content_types = None,
    state: User.State = None,
    send_user: bool = False,
    run_task = None,
    err_callback: callable = None,
    **err_callback_kwargs):
    """Функция хэндлинга сообщений.
    Реализует бд-стэйты, коллбэк-функции и сендинг юзера в функцию.

    Args:
        dispatcher (_type_): диспетчер бота
        commands (_type_, optional): комманды/ы. Defaults to None.
        regexp (_type_, optional): регексп. Defaults to None.
        content_types (_type_, optional): ... . Defaults to None.
        state (User.State, optional): стэйт доступа к функции. при несовпадении со стэйтом юзера зовет err_callback. Defaults to None.
        send_user (bool, optional): отсылать ли юзера в функцию(сокращение запросов в бд + меньше кода). Defaults to False.
        run_task (_type_, optional): _description_. Defaults to None.
        err_callback (callable, optional): функция которая вызывается в случае несовпадения стэйта юзера с запрошенным. Defaults to None.
    """    
    def decorator(foo: callable):

        nonlocalarg: Optional[Any] = None
        if send_user:
            class nonlocal_arg:
                ...
            nonlocalarg = nonlocal_arg()

        custom_state_filter = lambda msg: True
        if state:
            def custom_state_filter(msg):
                # nonlocal nonlocalarg
                return \
                state_requiered(
                    msg=msg,
                    req_state=state,
                    send_user=(send_user, nonlocalarg),
                    err_callback=err_callback,
                    message=msg,
                    **err_callback_kwargs)

        @dispatcher.message_handler(
            custom_state_filter,
            commands=commands,
            regexp=regexp,
            content_types=content_types,
            run_task=run_task)
        def wrapper(*args, **kwargs):
            # nonlocal nonlocalarg
            if send_user:
                if state:
                    return foo(*args, user=nonlocalarg.user, exists=nonlocalarg.exists)
                user, exists = User.get_or_create_by_msg(args[0])
                exists = not exists
                return foo(*args, user=user, exists=exists)
            return foo(*args)
        return wrapper
    return decorator
