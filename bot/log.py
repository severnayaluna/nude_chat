import logging


def get_logger(name: str) -> logging.Logger:
    """
    Возвращает сконфигурированный логер по имени name.
    """
    logger: logging.Logger = logging.getLogger(__name__)
    return logger
