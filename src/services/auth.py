from aiogram import types

from models import User

from log import get_logger, log_exceptions


logger = get_logger(__name__)


@log_exceptions(logger)
def reg_or_login(message: types.Message):
    user = message.from_user
    logger.info(f'User {user.id} tried to log/reg.')

    if user.is_bot:
        logger.warning(f'User {user.id} was bot.')
        return 'You cannot registarte a bot!'
    
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
        logger.error(ex)
        return f'We are running into an Unbound error:\n{ex.text}'    
