from typing import Any, Callable

import logging

from aiogram import types


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

                await ex.send_to_user(args[0])

        return wrapper
    
    return decorator


class BaseExceptionNotificationLevel:
    ...

class NotSendAtAllLevel(BaseExceptionNotificationLevel):
    @classmethod
    def get_error_text(cls, exception) -> None:
        return None

class SendUnboundErrorLevel(BaseExceptionNotificationLevel):
    @classmethod
    def get_error_text(cls, exception) -> str:
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
    def __init__(self, *args, notification_level: BaseExceptionNotificationLevel = NotSendAtAllLevel, **kwargs) -> None:
        self.notification_level: BaseExceptionNotificationLevel = notification_level

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
    
    async def send_to_user(self, message: types.Message):
        text = self.notification_level.get_error_text(self)
        if text:
            await message.reply(text)


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
