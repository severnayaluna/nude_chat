import sys

import asyncio

import logging

from aiogram import Bot, Dispatcher

from redis.asyncio import Redis

from bot.handlers import user_commands

from bot.config import Config
from bot.log import get_logger, configurate


logger = get_logger(__name__)


async def main() -> None:
    env_path, log_level = sys.argv[1], sys.argv[2]

    configurate(log_level, 'bot.log', 'w')

    config = Config(env_path)

    redis_storage = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
    logger.info(f'Redis running on {config.REDIS_HOST}:{config.REDIS_PORT}')
    await redis_storage.flushall()

    bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
    logger.info('Bot was created successfully')

    dp = Dispatcher(redis_storage=redis_storage)
    dp.include_routers(
        user_commands.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    logger.warning('Start polling')
    await dp.start_polling(bot)
    logger.warning('Stop polling')

    await redis_storage.aclose()


if __name__ == '__main__':
    asyncio.run(main())