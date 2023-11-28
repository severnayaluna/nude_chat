from aiogram import Bot, Dispatcher, types

import settings

from templates import greets

from services import auth, rooms

from models import User

from services.query import Room


Renderer = settings.RENDERER

bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher(bot)

logger = settings.logger


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        Renderer(
            message.from_user.username,
            settings.BOT_NAME,
            settings.HELP_COMMAND,
            text = greets.greet_text))


@dp.message_handler(commands=['reg'])
async def reg(message: types.Message):
    rendered_text = auth.reg_or_login(message)
    await message.reply(rendered_text)


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
                text = greets.in_room
            ))

        await bot.send_message(
            user2.tgid,
            Renderer(
                user2.name,
                text = greets.in_room
            ))

@dp.message_handler()
async def default_message(message: types.Message):
    user = message.from_user

    if Room.in_room(user.id):
        await bot.send_message(
            Room.redirect_from(user.id),
            message.text)
    else:
        await message.reply('You aren\'t in room yet!')
