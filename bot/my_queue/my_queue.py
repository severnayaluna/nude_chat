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



class Room:
    def __init__(self, storage: Redis) -> None:
        self.storage = storage

    async def try_create_room(self, queue: Queue) -> None | tuple[int, int]:
        pair = await queue.get_pair()
        if pair:
            id1, id2 = pair
            await self.storage.set(f'from_{id1}', id2)
            await self.storage.set(f'from_{id2}', id1)
            return pair
        return None

    async def redirect_from(self, id_: int | str) -> int | None:
        id2 = await self.storage.get(f'from_{id_}')
        if id2:
            return int(id2)
        return None

    async def delete_room(self, id_: int | str) -> bool:
        id2 = await self.storage.get(f'from_{id_}')

        if not id2:
            return False

        await self.storage.delete(f'from_{id_}')
        await self.storage.delete(f'from_{id2}')
        return True

    async def user_in(self, id_: int | str) -> bool:
        return await self.storage.get(f'from_{id_}') is not None
