from typing import Optional, Union

from .exceptions import NoPairsInQueue, DuplicateUser


class Room:
    __last_room_id = 0

    @classmethod
    def create_room_id(cls):
        cls.__last_room_id += 1
        return cls.__last_room_id


    def __init__(self, first_user: int, second_user: int):
        if first_user == second_user:
            raise DuplicateUser
        
        self.users = {
            'room_id': self.__class__.create_room_id(),
            'user_1': first_user,
            'user_2': second_user,
        }


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
