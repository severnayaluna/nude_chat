from models import User
from .custom_state.lambdas import state_requiered


def send_user_to_foo_by_msg(foo: callable):
    """Добавление юзера в аргументы функции(foo),
    посредством его получения/создания в бд по
    айди отправителя сообщения.

    Args:
        foo (callable): принимаемая функция
    """    
    def wrapper(*args, **kwargs):
        user, exists = User.get_or_create_by_msg(args[0])
        res = foo(*args, user=user, exists=not exists)
        return res
    
    return wrapper


def my_msg_handler(
    dispatcher,
    commands = None,
    regexp = None,
    content_types = None,
    state: User.State = None,
    run_task = None,
    err_callback: callable = None,
    **err_callback_kwargs):
    def decorator(foo: callable):
        @dispatcher.message_handler(
            lambda msg:
                state_requiered(
                    msg=msg,
                    req_state=state,
                    err_callback=err_callback,
                    message=msg,
                    **err_callback_kwargs),
                commands=commands,
                regexp=regexp,
                content_types=content_types,
                run_task=run_task)
        def wrapper(*args, **kwargs):
            return foo(*args)
        return wrapper
    return decorator
