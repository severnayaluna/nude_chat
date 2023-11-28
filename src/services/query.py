from typing import Optional, Union

from .exceptions import NoPairsInQueue, DuplicateUser


class Room:
    __rooms = {}
    @classmethod
    def cascade_create(cls, id1, id2):
        room1 = {str(id1): str(id2)}
        room2 = {str(id2): str(id1)}

        cls.__rooms.update(room1)
        cls.__rooms.update(room2)

    @classmethod
    def cascade_delete(cls, id):
        id2 = cls.__rooms[str(id)]
        
        cls.__rooms.pop(str(id))
        cls.__rooms.pop(str(id2))


    def __init__(self, first_user: int, second_user: int):
        if first_user == second_user:
            raise DuplicateUser
        
        self.__class__.cascade_create(first_user, second_user)
    
    @classmethod
    def redirect_from(cls, id):
        return cls.__rooms[str(id)]
    
    @classmethod
    def in_room(cls, id):
        return str(id) in cls.__rooms


class Queue:
    @property
    def queue(self) -> list[int]:
        return self.__users

    def __init__(self, users: Optional[list[int]] = None) -> None:
        if users:
            if sorted(set(users)) != sorted(users):
                raise DuplicateUser
            self.__users: list[int] = users
        else:
            self.__users: list[int] = []
    
    def get_pair(self) -> Union[NoPairsInQueue, tuple[int, int]]:
        try:
            first_user: int = self.__users[0]
            second_user: int = self.__users[1]
            self.__users.remove(first_user)
            self.__users.remove(second_user)
        except IndexError:
            raise NoPairsInQueue
        return first_user, second_user
    
    def put(self, user: int) -> None:
        if user in self.__users:
            raise DuplicateUser
        self.__users.append(user)
