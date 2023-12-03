from typing import Union

import logging

from aiogram import Bot, Dispatcher, types

import settings

from models import User

from services import auth, rooms
from services.query import Rooms
from services.msg_parser import parse_content
from services.exceptions import UnboundError, handle_exceptions, UserIsBot

from log import get_logger


if settings.BOT_TOKEN:
    bot = Bot(settings.BOT_TOKEN)
    dp = Dispatcher(bot)
else:
    raise UnboundError(f'There are no BOT_TOKEN!')

logger: logging.Logger = get_logger(__name__)


@dp.message_handler(commands=['start'])
@handle_exceptions(logger)
async def start(message: types.Message):
    """
    Хэндлер команды /start.

    Логика:
        - Вызывает в себе auth.reg_or_login.
    """
    logger.info(f'User {message.from_user.id} started bot.')
    
    rendered_text: str = auth.reg_or_login(message)
    
    await message.reply(rendered_text)
    await message.reply(f'Hello, {message.from_user.first_name}.\nThis is NoNudesChatRoulette bot.')


@dp.message_handler(commands=['find'])
@handle_exceptions(logger)
async def find_room(message: types.Message):
    """
    Хэндлер команды /find.

    Логика:
        - Вызывает в себе rooms.add_user_to_queue.
        - Вызывает в себе rooms.add_to_room_if_can.
        - Вызывает в себе User.get 2 раза.
    """
    logger.info(f'User {message.from_user.id} tried to add to queue.')

    text: str = rooms.add_user_to_queue(message)
    await message.reply(text)

    pair: Union[tuple[int, int], bool] = rooms.add_to_room_if_can()

    if pair:
        user1: User
        user2: User
        user1, user2 = User.get(tgid=pair[0]), User.get(tgid=pair[1])
        
        await bot.send_message(user1.tgid, text=f'Hey, {user1.name}, you are in room with {user2.name} now!')
        await bot.send_message(user2.tgid, text=f'Hey, {user2.name}, you are in room with {user1.name} now!')


@dp.message_handler(commands=['leave'])
@handle_exceptions(logger)
async def leave_room(message: types.Message):
    """
    Хэндлер команды /leave.

    Логика:
        - Вызывает в себе rooms.remove_user_from_room.
    """
    user: types.User = message.from_user

    logger.info(f'User {user.id} tried to leave room.')

    user1_text, user2_text, user1_id, user2_id = rooms.remove_user_from_room(message)

    if user1_id and user2_id and user1_text and user2_text:
        await bot.send_message(user1_id, user1_text)
        await bot.send_message(user2_id, user2_text)
    else:
        await message.reply(user1_text)



@dp.message_handler(commands=['exit'])
@handle_exceptions(logger)
async def exit_queue(message: types.Message):
    """
    Хэндлер команды /exit.

    Логика:
        - Вызывает в себе rooms.remove_user_from_queue.
    """
    logger.info(f'User {message.from_user.id} tried to leave queue.')

    text: str = rooms.remove_user_from_queue(message)
    await message.reply(text)


@dp.message_handler(content_types=['any'])
@handle_exceptions(logger)
async def default_message(message: types.Message):
    """
    Хэндлер любого сообщения не являющегося командой.

    Логика:
        - Вызывает в себе parse_content.
        - Вызывает в себе Rooms.redirect_from.
    """
    user: types.User = message.from_user

    file_id: str
    foo_name: str
    file_id, foo_name = parse_content(message)
    
    resend = getattr(bot, foo_name)

    if Rooms.in_room(user.id):
        reciever: dict = Rooms.redirect_from(user.id)

        logger.info(f'User {user.first_name} tried to {foo_name} - {file_id}, to {reciever["name"]}.')

        await bot.send_message(reciever['id'], text=user.first_name + ':')
        await resend(
            reciever['id'],
            file_id)
    else:
        await message.reply('You aren\'t in room yet!')
