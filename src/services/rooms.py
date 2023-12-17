from typing import Union, Optional

from aiogram import types

from services.validator import validate_msg

from .exceptions import *

from .query import Rooms, Queue

from log import get_logger


logger = get_logger(__name__)


def add_user_to_queue(message: types.Message) -> str:
    """
    Добавляет юзера в очередь.

    Если юзер - бот - возвращает исключение UserIsBot.
    """
    validate_msg(message)

    user: types.User = message.from_user

    if user.is_bot:
        raise UserIsBot(f'Sorry, {user.first_name}, but you can\'t add bot in queue!', logging_level=logging.WARNING)

    Queue.put(user.id)
    return f'{user.first_name}, you are in queue now.\nWait for free room...\nTo exit queue type /exit'


def remove_user_from_queue(message: types.Message) -> str:
    """
    Удаляет юзера из очереди.

    Если юзер - бот - возвращает исключение UserIsBot.
    """
    validate_msg(message)

    user: types.User = message.from_user

    if user.is_bot:
        raise UserIsBot(f'Can\'t remove bot from queue!', logging_level=logging.WARNING)

    Queue.remove(user.id)
    return f'{user.first_name}, you aren\'t in queue now.'


def remove_user_from_room(message: types.Message) -> tuple[str, Optional[str], Optional[int], Optional[int]]:
    """
    Удаляет юзера из комнаты.

    Если юзер - бот - возвращает исключение UserIsBot.
    """
    validate_msg(message)

    user: types.User = message.from_user

    if user.is_bot:
        raise UserIsBot(f'Can\'t remove bot from room!', logging_level=logging.WARNING)

    try:
        user2: dict = Rooms.redirect_from(user.id)
        Rooms.cascade_delete(user.id)

        return (
            f'{user.first_name}, you aren\'t in room now.',
            f'{user2["name"]}, your opponent leaved room.',
            int(user.id),
            int(user2['id'])
            )

    except NoSuchUser:
        return (
            'You aren\'t in room yet!',
            None,
            None,
            None
            )


def add_to_room_if_can() -> Union[tuple[int, int], bool]:
    """
    Создает комнату для пары юзеров елси может,
    в противном случае возвращает исключение NoPairsInQueue.
    """
    try:
        pair: tuple[int, int] = Queue.get_pair()
        Rooms(*pair)
        return pair

    except NoPairsInQueue:
        return False
