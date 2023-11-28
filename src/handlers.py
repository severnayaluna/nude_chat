from typing import Any
from aiogram import Bot, Dispatcher, types

import settings

from templates import greets

from services import auth, rooms

from models import User

from services.query import Room
from services.msg_parser import parse_content

from templates import exceptions


Renderer = settings.RENDERER

bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher(bot)

logger = settings.logger


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    rendered_text = auth.reg_or_login(message)
    await message.reply(rendered_text)

    await message.reply(
        Renderer(
            message.from_user.username,
            settings.BOT_NAME,
            settings.HELP_COMMAND,
            text = greets.greet_text))


@dp.message_handler(commands=['find'])
async def find_room(message: types.Message):
    text = rooms.add_user_to_queue(message)
    await message.reply(text)

    logger.info(f'{settings.QUEUE.queue}')
    pair = rooms.add_to_room_if_can()
    logger.info(f'{pair}, {settings.QUEUE.queue}')

    if pair:
        user1, user2 = User.get(tgid=pair[0]), User.get(tgid=pair[1])

        await bot.send_message(
            user1.tgid,
            Renderer(
                user1.name,
                text = greets.in_room))

        await bot.send_message(
            user2.tgid,
            Renderer(
                user2.name,
                text = greets.in_room))


@dp.message_handler(commands=['leave'])
async def leave_room(message: types.Message):
    user = message.from_user

    if Room.in_room(user.id):

        user2 = Room.redirect_from(user.id)
        await message.reply('You leaved room!')
        await bot.send_message(user2, 'Your opponent leaved room!')

        Room.cascade_delete(user.id)
    else:
        await message.reply(
            Renderer(
                'You aren\'t in room yet!',
                text = exceptions.exception_text))


@dp.message_handler(content_types=['any'])
async def default_message(message: types.Message):
    user = message.from_user

    file_id, foo_name = parse_content(message)
    resend = getattr(bot, foo_name)

    logger.info(f'{resend}; {file_id}')

    if Room.in_room(user.id):
        logger.info(f'{user.username} sended {message.text} to {Room.redirect_from(user.id)}')

        await resend(
            Room.redirect_from(user.id),
            file_id)
    else:
        await message.reply('You aren\'t in room yet!')
