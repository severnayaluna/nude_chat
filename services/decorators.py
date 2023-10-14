from models import User


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
