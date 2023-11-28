from aiogram.utils import executor

import settings

import handlers


logger = settings.logger


if __name__ == '__main__':
    logger.info('Bot started polling.')
    try:
        executor.start_polling(handlers.dp, skip_updates=True)
    except Exception as ex:
        logger.error(ex)
