import asyncio

from redis.asyncio import Redis

from bot import config


async def main() -> None:
    redis_storage = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    pair_iterator = redis_storage.scan_iter(count=2, match='user_*')
    user1, user2 = await anext(pair_iterator), await anext(pair_iterator)


asyncio.run(main())
