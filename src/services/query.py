from typing import Union

from .exceptions import *

from log import get_logger

from models import User


logger = get_logger(__name__)

class Rooms:
    """
    Класс *комнат*.
    Хранит пары связанных словарей(комнат):

        {
            'айди юзера 1': {
                'id': 'айди юзера 2'
                'name': 'имя юзера 2'
            }
        }

        {
            'айди юзера 2': {
                'id': 'айди юзера 1'
                'name': 'имя юзера 1'
            }
        }

    """
    __rooms = {}

    @classmethod
    def check_in_room(cls, id):
        """
        Если в комнатах не имеется такового юзер-айди,
        возвращает исключение NoSuchUser.
        """
        if not(cls.in_room(id)):
            ex = NoSuchUser(f'No such user in rooms!')
            ex.log_me(logger)
            raise ex
    
    @classmethod
    def cascade_create(cls, id1, id2):
        """
        Создает связанные словари(комнаты) по двум айди.
        """
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
        """
        Удаляет связанные словари(комнаты) по айди 1-го из юзеров.
        """
        cls.check_in_room(id)

        id2 = cls.__rooms[str(id)]
        
        cls.__rooms.pop(str(id))
        cls.__rooms.pop(str(id2))

    def __init__(self, first_user: int, second_user: int):
        """
        Вызывает cascade_create для пары юзер-айди.

        Если оба юзер-айди являются одним-и-тем-же юзер-айди,
        возвращает исключение SameUserError.

        Если один из юзер-айди уже находится в комнате,
        возвращает исключение DuplicateUser.
        """
        if first_user == second_user:
            ex = SameUserError(f'Can\'t create room with 2 same users!')
            ex.log_me(logger)
            raise ex
        
        if self.__class__.in_room(first_user) or self.__class__.in_room(second_user):
            ex = DuplicateUser(f'first_user or second_user already in rooms!')
            ex.log_me(logger)
            raise ex
        
        self.__class__.cascade_create(first_user, second_user)
    
    @classmethod
    def redirect_from(cls, id):
        """
        Возвращает айди юзера 2, к которому нужно редиректить сообщения, от юзера 1.
        """
        cls.check_in_room(id)

        return cls.__rooms[str(id)]
    
    @classmethod
    def in_room(cls, id):
        """
        Проверяет есть ли юзер с данным айди в комнатах
        (Проверяет является данное айди ключом одной из комнат).
        """
        return str(id) in cls.__rooms


class Queue:
    """
    Класс очереди.
    Хранит айди юзеров.
    """
    __users = []

    @classmethod
    @property
    def queue(cls) -> list[int]:
        """
        Возвращает все айди юзеров хранящиеся в очереди на данный момент.
        !!! Настоятельно не рекомендуется вручную менять что либо в переменной __users !!!
        """
        return cls.__users
    
    @classmethod
    def get_pair(cls) -> Union[NoPairsInQueue, tuple[int, int]]:
        """
        Возвращает первую пару юзер-айди если таковая имеется в очереди,
        иначе возвращает исключение NoPairsInQueue.
        """
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
        """
        Добавляет юзер-айди в очередь.

        Если такой юзер-айди уже имеется в очереди,
        возвращает исключение DuplicateUser.
        """
        if user in cls.__users:
            ex = DuplicateUser(f'You are already in queu!')
            ex.log_me(logger)
            raise ex
        cls.__users.append(user)

    @classmethod
    def remove(cls, user: int) -> None:
        """
        Удаляет юзер-айди из очереди, если таковой там имеется,
        в противном случае возвращает исключение NoSuchUser.
        """
        if user not in cls.__users:
            ex = NoSuchUser(f'No such user in queue!')
            ex.log_me(logger)
            raise ex
        
        return cls.__users.remove(user)
