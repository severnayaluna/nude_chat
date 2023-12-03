from aiogram import types

from services.validator import validate_msg

from .exceptions import *

from .query import Rooms, Queue

from log import get_logger


logger = get_logger(__name__)


def add_user_to_queue(message: types.Message):
    """
    Добавляет юзера в очередь.

    Если юзер - бот - возвращает исключение UserIsBot.
    """
    validate_msg(message)

    user = message.from_user

    if user.is_bot:
        raise UserIsBot(f'Sorry, {user.first_name}, but you can\'t add bot in queue!')
            
    user_id = user.id

    Queue.put(user_id)
    return f'{user.first_name}, you are in queue now.\nWait for free room...\nTo exit queue type /exit'


def remove_user_from_queue(message: types.Message):
    """
    Удаляет юзера из очереди.

    Если юзер - бот - возвращает исключение UserIsBot.
    """
    validate_msg(message)

    user = message.from_user

    if user.is_bot:
        raise UserIsBot(f'Can\'t remove bot from queue!')
            
    user_id = user.id

    Queue.remove(user_id)
    return f'{user.first_name}, you aren\'t in queue now.'


def remove_user_from_room(message: types.Message):
    """
    Удаляет юзера из комнаты.

    Если юзер - бот - возвращает исключение UserIsBot.
    """
    validate_msg(message)

    user = message.from_user

    if user.is_bot:
        raise UserIsBot(f'Can\'t remove bot from room!')

    if Rooms.in_room(user.id):
        user2 = Rooms.redirect_from(user.id)
        Rooms.cascade_delete(user.id)
        return (
            f'{user.first_name}, you aren\'t in room now.',
            f'{user2.name}, your opponent leaved room.',
            user.id,
            user2.tgid
            )

    else:
        return (
            'You aren\'t in room yet!',
            None,
            None,
            None
            )


def add_to_room_if_can():
    """
    Создает комнату для пары юзеров елси может,
    в противном случае возвращает исключение NoPairsInQueue.
    """
    try:
        pair = Queue.get_pair()
        Rooms(*pair)
        return pair

    except NoPairsInQueue:
        return False
