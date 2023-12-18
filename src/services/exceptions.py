from typing import Any, Callable

import logging


def handle_exceptions(logger: logging.Logger) -> Callable:
    """
    Декоратор для отлавливания ошибок в хэндлерах.
    Логирует ошибки и отправляет юзеру удобоваримый ответ.
    """
    def decorator(function: Callable) -> Callable:
        async def wrapper(*args, **_) -> Any:
            try:
                return await function(*args)

            except MyBaseException as ex:
                logger.log(ex.logging_level, ex)

                json_ex: dict = ex.json()
                await args[0].reply(
                    f'Error - {json_ex["name"]}:\n{json_ex["text"]}'
                )

        return wrapper

    return decorator


class BaseExceptionNotificationLevel:
    ...

class NotSendAtAllLevel(BaseExceptionNotificationLevel):
    @classmethod
    def get_error_text(cls, _) -> None:
        return None

class SendUnboundErrorLevel(BaseExceptionNotificationLevel):
    @classmethod
    def get_error_text(cls, _) -> str:
        return 'Извините, что-то пошло не так.\nПожалуйста, попробуйте еще раз позже.'

class SendFullErrorLevel(BaseExceptionNotificationLevel):
    @classmethod
    def get_error_text(cls, exception) -> str:
        json_ex = exception.json()
        return f'Error - {json_ex["name"]}:\n{json_ex["text"]}'

class SendOnlyTextLevel(BaseExceptionNotificationLevel):
    @classmethod
    def get_error_text(cls, exception) -> str:
        return exception.json()["text"]


class MyBaseException(Exception):
    """
    Базовый класс exception, от него надо наследовать все кастомные ошибки.
    """
    def __init__(
        self, notification_level: BaseExceptionNotificationLevel = NotSendAtAllLevel,
        logging_level = logging.ERROR) -> None:
        self.notification_level: BaseExceptionNotificationLevel = notification_level
        self.logging_level = logging_level

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
