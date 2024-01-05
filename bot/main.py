import asyncio

from aiogram import Bot, Dispatcher

from handlers import user_commands

import config
from log import get_logger


logger = get_logger(__name__)


async def main():
    bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
    logger.info('Bot was created successfully')
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
