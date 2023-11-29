from aiogram import types

from models import User

import settings


logger = settings.logger


def reg_or_login(message: types.Message):
    user = message.from_user
    if user.is_bot:
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
            return f'Hey, {db_user.name}, you successfully registrated in bot!'
        else:
            return f'Hey, {db_user.name}, you successfully logined in bot!'

    except Exception as ex:
        logger.error(ex)
        return f'We are running into an Unbound error:\n{ex.text}'    
