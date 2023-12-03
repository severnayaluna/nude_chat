import logging


def get_logger(name: str):
    """
    Возвращает сконфигурированный логер по имени name.
    """
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
    """
    Декоратор, который
    Отлавливает -> Логирует -> Вызывает,
    исключения возникшие в функции к кторой он был применен.
    """
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
    """
    Чистит файл логов.
    """
    with open('bot.log', 'w') as f:
        ...
