import logging


def get_logger(name: str) -> logging.Logger:
    """
    Возвращает сконфигурированный логер по имени name.
    """
    logging.basicConfig(
        filename = 'bot.log',
        filemode = 'a',
        level = logging.DEBUG,
        datefmt = '%m/%d/%Y %I:%M:%S %p')


    logger: logging.Logger = logging.Logger(name, level=logging.DEBUG)

    formatter: logging.Formatter = logging.Formatter(
        '%(name)s ~$ [ %(levelname)s ](%(asctime)s) - %(message)s')

    stream_handler: logging.Handler = logging.StreamHandler()
    file_handler: logging.Handler = logging.FileHandler(
        filename = 'bot.log',
        mode = 'a')

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
