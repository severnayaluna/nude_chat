import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from models import User, Room
from services.custom_state.lambdas import state_requiered
from services.decorators import send_user_to_foo_by_msg

from dotenv import load_dotenv

import os


logging.basicConfig(
    filename='bot.log',
    filemode='w',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p')

formatter = logging.Formatter(
    '%(name)s ~$ [ %(levelname)s ](%(asctime)s) - %(message)s')

logger = logging.getLogger()

handler = logging.StreamHandler()
file_handler = logging.FileHandler(
    filename='bot.log',
    mode='a')

file_handler.setFormatter(formatter)
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(file_handler)


project_folder = os.path.expanduser(os.getcwd())
load_dotenv(os.path.join(project_folder, '.env'))
logger.info('Loaded .env.')


def get_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))
    kb.add(KeyboardButton('/help'))
    return kb


bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)
logger.info('Bot and dp was created.')



@dp.message_handler(commands=['start'])
@send_user_to_foo_by_msg
async def cmd_start(message: types.Message, user: User, exists: bool):
    if not user.state == User.State.ended:
        await message.reply("Приветствую, дорогой друг \nНажми /create для создания профиля", reply_markup=get_kb())
    else:
        await message.reply("Приветствую, дорогой друг", reply_markup=get_kb())
 


@dp.message_handler(commands='create')
@send_user_to_foo_by_msg
async def create_profile(message: types.Message, user: User, exists: bool):
    logger.info(f'User {user.tgid} exists: {exists}!')
    if exists:
        if user.reg:
            user.set_state(User.State.ended)
            await message.reply('Ваш профиль уже создан!')
            return
        if user.name:
            user.set_state(User.State.age)
            logger.info(f'User {user.tgid} age!')
            return
        if user.age:
            user.set_state(User.State.description)
            logger.info(f'User {user.tgid} desc!')
            return

    await message.reply(f'Давайте создадим Ваш профиль!\nДля начала отправьте свое имя')
    user.set_state(User.State.name)
    logger.info(f'User {user.tgid} name!')


@dp.message_handler(
    lambda msg:
    state_requiered(
        msg=msg,
        req_state=User.State.name))
@send_user_to_foo_by_msg
async def create_profile(message: types.Message, user: User, exists: bool):
    error = user.set_name(message.text)
    if error:
        await message.reply(f'Ошибка в имени - {error}')   
        return
 
    user.set_state(User.State.age)
    await message.reply('Отправьте свой возраст.')


@dp.message_handler(
    lambda msg:
    state_requiered(
        msg=msg,
        req_state=User.State.age))
@send_user_to_foo_by_msg
async def create_profile(message: types.Message, user: User, exists: bool):
    error = user.set_age(message.text)
    if error:
        await message.reply(f'Ошибка в возрасте - {error}')   
        return
 
    user.set_state(User.State.description)
    await message.reply('Теперь отправьте описание.')


@dp.message_handler(
    lambda msg:
    state_requiered(
        msg=msg,
        req_state=User.State.description))
@send_user_to_foo_by_msg
async def create_profile(message: types.Message, user: User, exists: bool):
    user.set_description(message.text)
    user.set_reg(True)
    user.set_state(User.State.ended)
    await message.reply('Профиль создан.')


async def profile_not_reg_error(errcbk_msg: types.Message):
    await errcbk_msg.reply(f'Профиль еще не создан!')


@dp.message_handler(
    lambda msg:
    state_requiered(
        msg=msg,
        req_state=User.State.ended,
        err_callback=profile_not_reg_error,
        errcbk_msg=msg),
        commands=['profile'])
@send_user_to_foo_by_msg
async def send_profile(message: types.Message, user: User, exists: bool):
    await message.reply(f'Ваш профиль:\n\
    Имя: {user.name}\n\
    Возраст: {user.age}\n\
    О себе: {user.description}\n\
    ')


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer("Команды бота: \n /help \n /create \n /start \n /urls")


if __name__ == '__main__':
    logger.info('Bot started polling.')
    executor.start_polling(dp, skip_updates=True)
