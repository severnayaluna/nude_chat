import logging


def get_logger(name: str):
    logging.basicConfig(
        filename = 'bot.log',
        filemode = 'a',
        level = logging.INFO,
        datefmt = '%m/%d/%Y %I:%M:%S %p')


    logger = logging.Logger(name, level=logging.INFO)

    formatter = logging.Formatter(
        '%(name)s ~$ [ %(levelname)s ](%(asctime)s) - %(message)s')

    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(
        filename = 'bot.log',
        mode = 'a')

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


def log_exceptions(logger: logging.Logger):
    def wrapper(foo: callable):
        def decorator(*args, **kwargs):
            try:
                return foo(*args, **kwargs)
            except Exception as ex:
                logger.error(f'Exception:\n{ex}\n\nFoo: {foo.__name__}\n\nArgs: {args}\nKwargs: {kwargs}')
                raise ex
        return decorator
    return wrapper

def clear_logs():
    with open('bot.log', 'w') as f:
        ...
