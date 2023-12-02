from typing import Union

from .exceptions import *

from log import get_logger

from models import User


logger = get_logger(__name__)

class Rooms:
    __rooms = {}
    
    @classmethod
    def cascade_create(cls, id1, id2):
        try:
            user1, user2 = User.get(tgid=int(id1)), User.get(tgid=int(id2))
        except Exception as ex:
            ex = UnboundError(ex.args[0])
            ex.log_me(logger)
            raise ex

        room1 = {
            str(id1):{
                'id': str(id2),
                'name': user2.name,
            }
        }

        room2 = {
            str(id2):{
                'id': str(id1),
                'name': user1.name,
            }
        }


        cls.__rooms.update(room1)
        cls.__rooms.update(room2)

    @classmethod
    def cascade_delete(cls, id):
        id2 = cls.__rooms[str(id)]
        
        cls.__rooms.pop(str(id))
        cls.__rooms.pop(str(id2))

    def __init__(self, first_user: int, second_user: int):
        if first_user == second_user:
            ex = SameUserError(f'Can\'t create room with 2 same users!')
            ex.log_me(logger)
            raise ex
        
        self.__class__.cascade_create(first_user, second_user)
    
    @classmethod
    def redirect_from(cls, id):
        return cls.__rooms[str(id)]
    
    @classmethod
    def in_room(cls, id):
        return str(id) in cls.__rooms


class Queue:
    __users = []

    @classmethod
    @property
    def queue(cls) -> list[int]:
        return cls.__users
    
    @classmethod
    def get_pair(cls) -> Union[NoPairsInQueue, tuple[int, int]]:
        try:
            first_user: int = cls.__users[0]
            second_user: int = cls.__users[1]
            cls.__users.remove(first_user)
            cls.__users.remove(second_user)
        except IndexError:
            ex = NoPairsInQueue(f'There are no free pair in queue!')
            ex.log_me(logger)
            raise ex

        return first_user, second_user
    
    @classmethod
    def put(cls, user: int) -> None:
        if user in cls.__users:
            ex = DuplicateUser(f'You are already in queu!')
            ex.log_me(logger)
            raise ex
        cls.__users.append(user)

    @classmethod
    def remove(cls, user: int) -> None:
        if user not in cls.__users:
            ex = NoSuchUser(f'No such user in queue!')
            ex.log_me(logger)
            raise ex
        
        return cls.__users.remove(user)
