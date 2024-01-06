from redis import Redis


class Queue:
    def __init__(self, storage: Redis) -> None:
        self.storage = storage

    def clear_storage(self) -> None:
        self.storage.flushall()

    def add_user(self, id_: int | str) -> bool:
        if not self.user_in(id_):
            self.storage.set(f'user_{id_}', '')
            return False
        return True

    def get_pair(self) -> None | tuple[int, int]:
        pair_iterator = self.storage.scan_iter(count=2, match='user_*')
        try:
            user1, user2 = next(pair_iterator), next(pair_iterator)
            self.storage.delete(user1, user2)
            return int(user1.split('user_')[-1]), int(user2.split('user_')[-1])

        except StopIteration:
            return None

    def remove_user(self, id_: int | str) -> bool:
        return bool(self.storage.delete(f'user_{id_}'))

    def close_connection(self) -> None:
        self.storage.close()

    def get_storage(self) -> Redis:
        return self.storage

    def user_in(self, id_: int | str) -> bool:
        return self.storage.get(f'user_{id_}') is not None



class Room:
    def __init__(self, storage: Redis) -> None:
        self.storage = storage

    def try_create_room(self, queue: Queue) -> None | tuple[int, int]:
        pair = queue.get_pair()
        if pair:
            id1, id2 = pair
            self.storage.set(f'from_{id1}', id2)
            self.storage.set(f'from_{id2}', id1)
            return pair
        return None

    def redirect_from(self, id_: int | str) -> int | None:
        id2 = self.storage.get(f'from_{id_}')
        if id2:
            return int(id2)
        return None

    def delete_room(self, id_: int | str) -> bool:
        id2 = self.storage.get(f'from_{id_}')

        if not id2:
            return False

        self.storage.delete(f'from_{id_}')
        self.storage.delete(f'from_{id2}')
        return True

    def user_in(self, id_: int | str) -> bool:
        return self.storage.get(f'from_{id_}') is not None
