import json

from typing import Iterable

from redis.asyncio import Redis

from ..log import get_logger


logger = get_logger(__name__)


class Queue:
    def __init__(self, storage: Redis) -> None:
        self.storage = storage

    async def clear_storage(self) -> None:
        await self.storage.flushall()

    async def add_user(self, id_: int | str) -> bool:
        if not await self.user_in(id_):
            await self.storage.set(f'user_{id_}', '')
            return False
        return True

    async def get_pair(self) -> None | tuple[int, int]:
        """deprecated:
            use 'get_group_of_users' instead

        Returns:
            None | tuple[int, int]: user ids
        """
        pair_iterator = self.storage.scan_iter(count=2, match='user_*')
        try:
            user1, user2 = await anext(pair_iterator), await anext(pair_iterator)
            await self.storage.delete(user1, user2)
            return int(user1.split('user_')[-1]), int(user2.split('user_')[-1])

        except StopAsyncIteration:
            return None

    async def remove_user(self, id_: int | str) -> bool:
        return bool(await self.storage.delete(f'user_{id_}'))

    async def get_storage(self) -> Redis:
        return self.storage

    async def user_in(self, id_: int | str) -> bool:
        return await self.storage.get(f'user_{id_}') is not None

    async def get_group_of_users(self, count: int) -> None | tuple[int]:
        iterator = self.storage.scan_iter(count=count, match='user_*')
        try:
            users: list[str] = [await anext(iterator) for _ in range(count)]
            if not len(users) == count:
                raise StopAsyncIteration

            await self.storage.delete(*users)
            return (int(user.split('user_')[-1]) for user in users)

        except StopAsyncIteration:
            return None



class Room:
    def __init__(self, storage: Redis) -> None:
        self.storage = storage

    # async def try_create_room(self, queue: Queue) -> None | tuple[int, int]:
    #     """deprecated:

    #     Args:
    #         queue (Queue): queue class

    #     Returns:
    #         None | tuple[int, int]: user ids
    #     """
    #     pair = await queue.get_pair()
    #     if pair:
    #         id1, id2 = pair
    #         await self.storage.set(f'from_{id1}', id2)
    #         await self.storage.set(f'from_{id2}', id1)
    #         return pair
    #     return None

    async def try_create_room(self, queue: Queue, people_count: int = 2) -> None | list[int]:
        users = await queue.get_group_of_users(count=people_count)
        if users:
            [
                await self.storage.set(f'from_{id_}', json.dumps(users[:idx] + users[idx+1:]))
                for idx, id_ in enumerate(users)
            ]
            return users
        else:
            return None

    async def redirect_from(self, id_: int | str) -> int | None | tuple[int]:
        reditect_to_ids = await self.storage.get(f'from_{id_}')

        if not reditect_to_ids: return reditect_to_ids
        reditect_to_ids: list = json.loads(reditect_to_ids)

        return tuple(map(int, reditect_to_ids))

    async def delete_room(self, id_: int | str) -> bool:
        ids = list(bytes(await self.storage.get(f'from_{id_}'), 'utf-8'))

        if not ids:
            return False

        [await self.storage.delete(f'from_{id_}') for id_ in ids]
        return True

    async def user_in(self, id_: int | str) -> bool:
        return await self.storage.get(f'from_{id_}') is not None
