from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from ..my_queue.my_queue import Queue, Room

from ..log import get_logger


logger = get_logger(__name__)
router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    logger.debug('Start')
    await message.reply(f'Hi, it\'s NoNudeChatRouletteBot.\nType /help to get available commands.')


@router.message(Command('find'))
async def find(message: Message, redis_storage, bot: Bot) -> None:
    queue = Queue(redis_storage)
    room = Room(redis_storage)

    in_search = await queue.add_user(message.from_user.id)
    if in_search: await message.reply('You arelready in search')

    pair = await room.try_create_room(queue=queue)

    if pair:
        await bot.send_message(pair[0], text=f'You are with {pair[1]} now!')
        await bot.send_message(pair[1], text=f'You are with {pair[0]} now!')
        return None
    else:
        await message.reply('Finding room...')


@router.message(Command('exit', 'exit_queue'))
async def exit_queue(message: Message, redis_storage, bot: Bot) -> None:
    queue = Queue(redis_storage)

    if await queue.user_in(id_:=message.from_user.id):
        await queue.remove_user(id_)
        await message.reply('You exited queue')
    else:
        await message.reply('You aren\'t in queue yet')


@router.message(Command('leave', 'leave_room'))
async def leave_room(message: Message, redis_storage, bot: Bot) -> None:
    room = Room(redis_storage)

    if await room.user_in(id_:=message.from_user.id):
        id2 = await room.redirect_from(id_)
        await message.reply('You leaved room')
        await bot.send_message(id2, text=f'Your opponent leaved')
    else:
        await message.reply('You aren\'t in room yet')


@router.message()
async def echo(message: Message, redis_storage, bot: Bot) -> None:
    room = Room(redis_storage)

    to_user_id = await room.redirect_from(message.from_user.id)
    if to_user_id:
        await bot.send_message(to_user_id, text=message.text)
        return
    await message.reply('You are not in room yet')
