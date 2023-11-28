from aiogram import types

import settings

from .exceptions import DuplicateUser, NoPairsInQueue

from templates import exceptions, greets

from .query import Room


Renderer = settings.RENDERER

logger = settings.logger

queue = settings.QUEUE


def add_user_to_queue(message: types.Message):
    user = message.from_user

    if user.is_bot:
        return Renderer(
            'Sorry, but you can\'t add bot in queue!',
            text = exceptions.exception_text
        )
    
    user_id = user.id

    try:
        queue.put(user_id)
        return Renderer(
            user.username,
            text = greets.successful_added_in_queue
        )
    
    except DuplicateUser as ex:
        return Renderer(
            'Yor are already in queue!',
            text = exceptions.exception_text
        )
    
    except Exception as ex:
        logger.error(ex)
        return Renderer(
            'Unbound error!',
            text = exceptions.exception_text
        )


def add_to_room_if_can():
    try:
        pair = queue.get_pair()
        Room(*pair)
        return pair

    except NoPairsInQueue as ex:
        return False
    
    except Exception as ex:
        logger.error(ex)
        return Renderer(
            'Unbound error!',
            text = exceptions.exception_text
        )