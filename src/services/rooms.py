from aiogram import types

import settings

from .exceptions import DuplicateUser, NoPairsInQueue, NoSuchUser

from .query import Rooms, Queue

from log import get_logger, log_exceptions


logger = get_logger(__name__)


@log_exceptions(logger)
def add_user_to_queue(message: types.Message):
    user = message.from_user

    if user.is_bot:
        return f'Sorry, {user.first_name}, but you can\'t add bot in queue!'
            
    user_id = user.id

    try:
        Queue.put(user_id)
        return f'{user.first_name}, you are in queue now.\nWait for free room...\nTo exit queue type /exit'
    
    except DuplicateUser as ex:
        return f'{user.first_name}, you are already in queue!'
    
    except Exception as ex:
        logger.error(ex)
        return f'We are running into an Unbound error:\n{ex.text}'


@log_exceptions(logger)
def remove_user_from_queue(message: types.Message):
    user = message.from_user

    if user.is_bot:
        return f'Sorry, {user.first_name}, but you can\'t remove bot from queue!'
            
    user_id = user.id

    try:
        Queue.remove(user_id)
        return f'{user.first_name}, you aren\'t in queue now.'
    
    except NoSuchUser as ex:
        return f'{user.first_name}, you aren\'t in queue!'
    
    except Exception as ex:
        logger.error(ex)
        return f'We are running into an Unbound error:\n{ex.text}'


@log_exceptions(logger)
def remove_user_from_room(message: types.Message):
    user = message.from_user

    if user.is_bot:
        return f'Sorry, {user.first_name}, but you can\'t remove bot from queue!'

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


@log_exceptions(logger)
def add_to_room_if_can():
    try:
        pair = Queue.get_pair()
        Rooms(*pair)
        return pair

    except NoPairsInQueue as ex:
        return False
    
    except Exception as ex:
        logger.error(ex)
        return f'We are running into an Unbound error:\n{ex}'
