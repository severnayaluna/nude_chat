from aiogram import types

from models import User

import settings

from templates import exceptions, greets


Renderer = settings.RENDERER

logger = settings.logger


def reg_or_login(message: types.Message):
    user = message.from_user
    if user.is_bot:
        return Renderer(
            'You cannot registarte a bot!',
            text = exceptions.exception_text
        )
    
    user_id = user.id
    username = user.username
    description = 'Without BIO'
    age = 18

    try:
        bd_user, _ = User.get_or_create(
            name = username,
            tgid = user_id,
            description = description,
            age = age)
        
        return Renderer(
            bd_user.name,
            text = greets.successful_auth
        )

    except Exception as ex:
        logger.error(ex)
        return Renderer(
            'Unbound error!',
            text = exceptions.exception_text
        )
    