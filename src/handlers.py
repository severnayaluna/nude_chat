from typing import Any

from aiogram import Bot, Dispatcher, types

import settings

from models import User

from services import auth, rooms
from services.query import Rooms, Queue
from services.msg_parser import parse_content


bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher(bot)

logger = settings.logger.getChild(__name__)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    logger.info(f'User {message.from_user.first_name} started bot.')
    
    rendered_text = auth.reg_or_login(message)
    
    await message.reply(rendered_text)
    await message.reply(f'Hello, {message.from_user.first_name}.\nThis is NoNudesChatRoulette bot.')


@dp.message_handler(commands=['find'])
async def find_room(message: types.Message):
    logger.info(f'User {message.from_user.first_name} tried to add to queue.')

    text = rooms.add_user_to_queue(message)
    await message.reply(text)

    pair = rooms.add_to_room_if_can()

    if pair:
        user1, user2 = User.get(tgid=pair[0]), User.get(tgid=pair[1])
        
        await bot.send_message(f'Hey, {user1.name}, you are in room with {user2.name} now!')
        await bot.send_message(f'Hey, {user2.name}, you are in room with {user1.name} now!')


@dp.message_handler(commands=['leave'])
async def leave_room(message: types.Message):
    user = message.from_user

    logger.info(f'User {user.first_name} tried to leave room.')

    user1_text, user2_text, user1_id, user2_id = rooms.remove_user_from_room(message)

    if user2_text:
        await bot.send_message(user1_id, user1_text)
        await bot.send_message(user2_id, user2_text)
    else:
        await message.reply(user1_text)



@dp.message_handler(commands=['exit'])
async def exit_queue(message: types.Message):
    logger.info(f'User {message.from_user.first_name} tried to leave queue.')

    text = rooms.remove_user_from_queue(message)
    await message.reply(text)


@dp.message_handler(content_types=['any'])
async def default_message(message: types.Message):
    user = message.from_user

    file_id, foo_name = parse_content(message)
    resend = getattr(bot, foo_name)

    if Rooms.in_room(user.id):
        await resend(
            Rooms.redirect_from(user.id),
            file_id)
    else:
        await message.reply('You aren\'t in room yet!')
