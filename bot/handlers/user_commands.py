from aiogram import Router, Bot, F
from aiogram.types import Message, User
from aiogram.filters import CommandStart, Command, CommandObject

from ..my_queue.my_queue import Queue, Room

# from ..middlewares.acess_middleware import AcessMiddleware
from ..middlewares.user_middleware import UserMiddleware

from logging import getLogger, Logger


# logger = getLogger(__name__)
logger = getLogger(__name__)
router = Router()

router.message.middleware(
    # AcessMiddleware([
    #     2021855860,
    # ]),
    UserMiddleware(),
)


@router.message(CommandStart())
async def start(message: Message) -> None:
    logger.debug(f'User {message.from_user.id} - /start')
    await message.reply(f'Hi, it\'s NoNudeChatRouletteBot.\nType /help to get available commands.')


@router.message(Command('help'))
async def help(message: Message) -> None:
    logger.debug(f'User {message.from_user.id} - /help')
    await message.reply('''
    Commands:
        /find <people in room count> - search for room
        /exit - exit searching
        /leave - leave from room
    ''')


@router.message(Command('find'))
async def find(message: Message, command: CommandObject, redis_storage, bot: Bot) -> None:
    msg_user_id = message.from_user.id
    try:
        count = int(command.args)
        logger.debug(f'User {msg_user_id} - /find {count}')
    except (TypeError, AttributeError, ValueError):
        logger.debug(f'User {msg_user_id} - /find !wrong_count!')
        await message.reply('Wrong count')
        return None

    queue = Queue(redis_storage)
    room = Room(redis_storage, queue)

    if await room.redirect_from(msg_user_id):
        logger.debug(f'User {msg_user_id} tryed to /find while beig in room - denied')
        await message.reply('You can\'t start search, while being in room!')
        return None

    in_search = await queue.get_or_create(msg_user_id, count)
    if in_search:
        logger.debug(f'User - {msg_user_id} was already in search')
        await message.reply('You arelready in search!')
    logger.debug(f'User - {msg_user_id} added to queue')

    users = await room.try_to_create_room(count)

    if users:
        logger.debug(f'Created room via {msg_user_id} with {count} peoples\nUsers: {users}')
        text = 'Room created, users:\n' + '\n'.join(map(str, users))
        for id_ in users:
            await bot.send_message(id_, text=text)
        return None
    else:
        logger.debug(f'Room was not created via {msg_user_id} - not enough people')
        await message.reply(f'Searching for room with {count} people...')


@router.message(Command('exit', 'exit_queue'))
async def exit_queue(message: Message, redis_storage, bot: Bot) -> None:
    msg_user_id = message.from_user.id

    logger.debug(f'User {msg_user_id} - /exit')

    queue = Queue(redis_storage)

    was_in_queue = await queue.remove_user(message.from_user.id)
    if was_in_queue:
        logger.debug(f'User {msg_user_id} exited queue')
        await message.reply('You exited queue')
    else:
        logger.debug(f'User {msg_user_id} was not in queue')
        await message.reply('You aren\'t in queue yet')


@router.message(Command('leave', 'leave_room'))
async def leave_room(message: Message, redis_storage, bot: Bot) -> None:
    msg_user_id = message.from_user.id

    logger.debug(f'User {msg_user_id} - /leave')

    queue = Queue(redis_storage)
    room = Room(redis_storage, queue)

    user_ids = await room.redirect_from(message.from_user.id)

    if user_ids:
        logger.debug(f'User {msg_user_id} leaved room')
        await room.delete_user(message.from_user.id)
        await message.reply('You leaved room')

        for id_ in user_ids:
            await bot.send_message(id_, f'{message.from_user.id} leaved room')
        return
    logger.debug(f'User {msg_user_id} was not in room')
    await message.reply('You aren\'t in room yet')


@router.message()
async def echo(message: Message, redis_storage, bot: Bot) -> None:
    msg_user_id = message.from_user.id

    logger.debug(f'User {msg_user_id} - echo:\n{message.text}')

    queue = Queue(redis_storage)
    room = Room(redis_storage, queue)

    redirect_to_ids = await room.redirect_from(message.from_user.id)
    if redirect_to_ids:
        logger.debug(f'Echo by {msg_user_id} was redirected to {[id_ for id_ in redirect_to_ids]}')
        if len(redirect_to_ids) > 1:
            redirect_to_ids.remove(msg_user_id)
        for id_ in redirect_to_ids:
            await bot.send_message(id_, text=message.text)
        return None
    logger.debug(f'Echo by {msg_user_id} was not redirected - not in room')
    await message.reply('You are not in room yet')
