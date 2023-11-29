from typing import Any

from aiogram import Bot, Dispatcher, types

import settings

from models import User

from services import auth, rooms
from services.query import Rooms, Queue
from services.msg_parser import parse_content


bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher(bot)

logger = settings.logger


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    rendered_text = auth.reg_or_login(message)
    
    await message.reply(rendered_text)
    await message.reply(f'Hello, {message.from_user.first_name}.\nThis is NoNudesChatRoulette bot.')


@dp.message_handler(commands=['find'])
async def find_room(message: types.Message):
    text = rooms.add_user_to_queue(message)
    await message.reply(text)

    logger.info(f'{Queue.queue}')
    pair = rooms.add_to_room_if_can()
    logger.info(f'{pair}, {Queue.queue}')

    if pair:
        user1, user2 = User.get(tgid=pair[0]), User.get(tgid=pair[1])

        await bot.send_message(f'Hey, {user1.name}, you are in room with {user2.name} now!')
        await bot.send_message(f'Hey, {user2.name}, you are in room with {user1.name} now!')


@dp.message_handler(commands=['leave'])
async def leave_room(message: types.Message):
    user = message.from_user

    if Rooms.in_room(user.id):

        user2 = Rooms.redirect_from(user.id)
        await message.reply('You leaved room!')
        await bot.send_message(user2, 'Your opponent leaved room!')

        Rooms.cascade_delete(user.id)
    else:
        await message.reply(f'You aren\'t in room yet!')


@dp.message_handler(content_types=['any'])
async def default_message(message: types.Message):
    user = message.from_user

    file_id, foo_name = parse_content(message)
    resend = getattr(bot, foo_name)

    logger.info(f'{resend}; {file_id}')

    if Rooms.in_room(user.id):
        logger.info(f'{user.username} sended {message.text} to {Rooms.redirect_from(user.id)}')

        await resend(
            Rooms.redirect_from(user.id),
            file_id)
    else:
        await message.reply('You aren\'t in room yet!')
