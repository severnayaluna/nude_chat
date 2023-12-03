from typing import Any, Callable

import logging


def handle_exceptions(logger: logging.Logger) -> Callable:
    """
    Декоратор для отлавливания ошибок в хэндлерах.
    Логирует ошибки и отправляет юзеру удобоваримый ответ.
    """
    def decorator(foo: Callable) -> Callable:
        async def wrapper(*args, **_) -> Any:
            try:
                return await foo(*args)
            
            except Exception as ex:
                ex: MyBaseException
                logger.error(ex)

                json_ex: dict = ex.json()
                await args[0].reply(
                    f'Error - {json_ex["name"]}:\n{json_ex["text"]}'
                )

        return wrapper
    
    return decorator


class MyBaseException(Exception):
    """
    Базовый класс exception, от него надо наследовать все кастомные ошибки.
    """
    def json(self: Exception) -> dict:
        """
        Конвертирует ошибку в json.
        """
        return {
            'name': self.__class__.__name__,
            'text': self.args[0],
        }
    
    def log_me(self, logger: logging.Logger) -> None:
        logger.error(self)


class NoPairsInQueue(MyBaseException):
    ...


class DuplicateUser(MyBaseException):
    ...


class NoSuchUser(MyBaseException):
    ...


class UserIsBot(MyBaseException):
    ...


class WrongType(MyBaseException):
    ...

class UnboundError(MyBaseException):
    ...

class SameUserError(MyBaseException):
    ...
