import json

from typing import Iterable

from redis.asyncio import Redis

from ..log import get_logger


logger = get_logger(__name__)


class Queue:
    def __init__(self, storage: Redis) -> None:
        self.storage = storage

    async def get_or_create(self, id_: int | str, people_count: int) -> bool:
        """"
        returns: user was in queue
        """
        if not await self.in_search(id_):
            await self.storage.set(f'search:{id_}:{people_count}', '')
            return False
        return True

    async def in_search(self, id_: int | str) -> bool:
        try:
            await anext(self.storage.scan_iter(match=f'search:{id_}:*', count=1))
            return True
        except StopAsyncIteration:
            return False

    async def get_group(self, count: int | str) -> None | list[int]:
        iterator = self.storage.scan_iter(match=f'search:*:{count}')
        try:
            users = [await anext(iterator) for _ in range(int(count))]
            await self.storage.delete(*users)

            return list(map(
                lambda s: int(s.split(':')[1]), users
            ))
        except StopAsyncIteration:
            return None

    async def remove_user(self, id_: int | str) -> bool:
        iterator = self.storage.scan_iter(match=f'search:{id_}:*', count=1)
        try:
            key = await anext(iterator)
            await self.storage.delete(key)
            return True
        except StopAsyncIteration:
            return False

class Room:
    def __init__(self, storage: Redis, queue: Queue) -> None:
        self.storage = storage
        self.queue = queue

    async def try_to_create_room(self, count: int | str) -> None | list[int]:
        logger.debug(f'try_to_create_room(count={count})')
        users = await self.queue.get_group(count)
        logger.debug(f'users - {users}')
        if users:
            sorted_str_users = list(map(str, sorted(users)))
            await self.storage.set(self.create_room_name(users), json.dumps(users))
            return users
        return None

    async def redirect_from(self, id_: int | str) -> None | list[int]:
        iterator = self.storage.scan_iter(match=f'from_*{id_}*', count=1)
        try:
            users = json.loads(await self.storage.get(await anext(iterator)))
            return users
        except StopAsyncIteration:
            return None

    async def delete_room(self, name: str) -> bool:
        if self.storage.exists(name):
            self.storage.delete(name)
            return True
        return False

    def create_room_name(self, ids: list[int]) -> str:
        return f'from_' + '_'.join(map(str, sorted(ids)))

    async def delete_user(self, id_: int | str) -> bool:
        users = await self.redirect_from(id_)
        if not users:
            return False

        room_name = self.create_room_name(users)

        if len(users) <= 2:
            await self.storage.delete(room_name)
            return True

        await self.storage.delete(room_name)
        users.remove(int(id_))
        await self.storage.set(self.create_room_name(users), json.dumps(users))

        return True
