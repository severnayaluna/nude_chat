# from typing import

from redis import Redis

from bot import config


class Queue:
    __storage = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)


    @classmethod
    def clear_storage(cls) -> None:
        cls.__storage.flushall()

    @classmethod
    def add_user(cls, id_: int | str) -> bool:
        if not cls.__storage.get(f'user_{id_}'):
            cls.__storage.set(f'user_{id_}', '')
            return False
        return True

    @classmethod
    def get_pair(cls) -> None | tuple[int, int]:
        pair_iterator = cls.__storage.scan_iter(count=2, match='user_*')
        try:
            user1, user2 = next(pair_iterator), next(pair_iterator)
            cls.__storage.delete(user1, user2)
            return int(user1.split('user_')[-1]), int(user2.split('user_')[-1])

        except StopIteration:
            return None

    @classmethod
    def remove_user(cls, id_: int | str) -> bool:
        return bool(cls.__storage.delete(f'user_{id_}'))

    @classmethod
    def close_connection(cls) -> None:
        cls.__storage.close()

    @classmethod
    def get_storage(cls) -> Redis:
        return cls.__storage



class Room:
    __storage = Queue.get_storage()
    __Queue = Queue

    @classmethod
    def try_create_room(cls) -> None | tuple[int, int]:
        pair = cls.__Queue.get_pair()
        if pair:
            id1, id2 = pair
            cls.__storage.set(f'from_{id1}', id2)
            cls.__storage.set(f'from_{id2}', id1)
            return pair
        return None

    @classmethod
    def redirect_from(cls, id_: int | str) -> int | None:
        id2 = cls.__storage.get(f'from_{id_}')
        if id2:
            return int(id2)
        return None

    @classmethod
    def delete_room(cls, id_: int | str) -> bool:
        id2 = cls.__storage.get(f'from_{id_}')

        if not id2:
            return False

        cls.__storage.delete(f'from_{id_}')
        cls.__storage.delete(f'from_{id2}')
        return True
