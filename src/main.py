from aiogram.utils import executor

from log import get_logger, log_exceptions

import handlers


logger = get_logger(__name__)

@log_exceptions(logger)
def main():
    executor.start_polling(handlers.dp, skip_updates=True)


if __name__ == '__main__':
    main()