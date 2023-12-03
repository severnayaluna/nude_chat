import logging

from aiogram.utils import executor

from log import get_logger, log_exceptions, clear_logs
clear_logs()

import handlers

from models import User

import settings


settings.MAIN_DB.create_tables([User,])

logger: logging.Logger = get_logger(__name__)

@log_exceptions(logger)
def main() -> None:
    executor.start_polling(handlers.dp, skip_updates=True)


if __name__ == '__main__':
    main()