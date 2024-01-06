import asyncio

from aiogram import Bot, Dispatcher

from redis import Redis

from handlers import user_commands

import config
from log import get_logger


logger = get_logger(__name__)

redis_storage = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)
redis_storage.flushall()
logger.info(f'Redis running on {config.REDIS_HOST}:{config.REDIS_PORT}')


async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
    logger.info('Bot was created successfully')
    dp = Dispatcher()
    dp['redis_storage'] = redis_storage

    dp.include_routers(
        user_commands.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info('Starting polling')
    await dp.start_polling(bot)
    redis_storage.close()


if __name__ == '__main__':
    asyncio.run(main())
