from aiogram import types

from models import User

from log import get_logger

from .exceptions import *
from services.validator import validate_msg

logger = get_logger(__name__)


def reg_or_login(message: types.Message):
    validate_msg(message)

    user = message.from_user
    logger.info(f'User {user.id} tried to log/reg.')

    if user.is_bot:
        ex = UserIsBot(f'You can\'t registrate/login a bot!')
        ex.log_me(logger)
        raise ex
    
    user_id = user.id
    username = user.first_name
    description = 'Without BIO'
    age = 18

    try:
        db_user, wasnt_in_db = User.get_or_create(
            name = username,
            tgid = user_id,
            description = description,
            age = age)
        
        if wasnt_in_db:
            logger.info(f'User {user.id} successfully registrated.')
            return f'Hey, {db_user.name}, you successfully registrated in bot!'
        else:
            logger.info(f'User {user.id} successfully logined.')
            return f'Hey, {db_user.name}, you successfully logined in bot!'

    except Exception as ex:
        ex = UnboundError(ex.args[0])
        ex.log_me(logger)
        raise ex
