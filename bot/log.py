import logging


def configurate(log_level, filename: str, mode: str) -> None:
    logging.basicConfig(
        level = log_level,
        datefmt = '%m/%d/%Y %I:%M:%S %p',
        format='[ %(levelname)s ](%(asctime)s):%(name)s$ %(message)s',
        handlers=(
            logging.StreamHandler(),
            logging.FileHandler(filename = 'bot.log', mode='w')
        ),
    )

def get_logger(name: str) -> logging.Logger:
    """
    Возвращает сконфигурированный логер по имени name.
    """
    logger: logging.Logger = logging.getLogger(__name__)
    return logger
