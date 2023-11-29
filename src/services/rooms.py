from aiogram import types

import settings

from .exceptions import DuplicateUser, NoPairsInQueue

from .query import Rooms, Queue


logger = settings.logger


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

def add_to_room_if_can():
    try:
        pair = Queue.get_pair()
        Rooms(*pair)
        return pair

    except NoPairsInQueue as ex:
        return False
    
    except Exception as ex:
        logger.error(ex)
        return f'We are running into an Unbound error:\n{ex.text}'