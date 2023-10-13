import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from models import User, Room
from services.model_services import *


from dotenv import load_dotenv

import os


logging.basicConfig(
    filename='bot.log',
    filemode='a',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p')

formatter = logging.Formatter(
    '[%(name)s](%(asctime)s) - %(levelname)s - %(message)s')

logger = logging.Logger(
    name='bot_logger',
    level=logging.INFO)

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



class UserState(StatesGroup):
    name = State()
    age = State()
    description = State()
    ended = State()


DataStorage = MemoryStorage()


def get_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))
    kb.add(KeyboardButton('/help'))
    return kb


bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot, storage=DataStorage)
logger.info('Bot and dp was created.')


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):

    if not UserState.ended:
        await message.reply("Приветствую, дорогой друг \nНажми /create для создания профиля", reply_markup=get_kb())
    else:
        await message.reply("Приветствую, дорогой друг", reply_markup=get_kb())
 

@dp.message_handler(commands='create')
async def create_profile(message: types.Message):
    user, exists = User.get_or_create(tgid=message.from_user.id)
    exists = not exists

    if exists:
        if user.name:
            await UserState.age.set()
            return
        if user.age:
            await UserState.description.set()
            return
        if user.description:
            await UserState.ended.set()
            return
    else:
        await UserState.name.set()

    await message.reply(f'Давайте создадим Ваш профиль!\nДля начала отправьте свое имя')


@dp.message_handler(state=UserState.name)
async def create_profile(message: types.Message):
    user = get_user(message)

    error = user.set_name(message.text)
    if error:
        await message.reply(f'Ошибка в имени - {error}')   
        return
 
    await message.reply('Отправьте свой возраст.')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def create_profile(message: types.Message):
    user = get_user(message)

    error = user.set_age(message.text)
    if error:
        await message.reply(f'Ошибка в возрасте - {error}')   
        return
 
    await message.reply('Теперь отправьте описание.')
    await UserState.description.set()


@dp.message_handler(state=UserState.description)
async def create_profile(message: types.Message):
    user = get_user(message)
    user.set_description(message.text)
    await message.reply('Профиль создан.')
    # user.reg = True
    user.save()
    await UserState.ended.set()


# @dp.message_handler(commands=['find'])
# async def cmd_find_room(message: types.Message):
#     user = get_user(message)
#     if not user.reg:
#         await message.reply('Для начала зарегайся /create !')
#         return


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer("Команды бота: \n /help \n /create \n /start \n /urls")


if __name__ == '__main__':
    logger.info('Bot started polling.')
    executor.start_polling(dp, skip_updates=True)
