import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from models import User, Room

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
    user, exists = User.get_or_create(tgid=message.from_user.id)

    if exists:
        if not user.decription:
            await UserState.description.set()
        if not user.age:
            await UserState.age.set()
        if not user.name:
            await UserState.name.set()

        if user.name and user.age and user.description:
            await UserState.ended.set()

    if not UserState.ended:
        await message.reply("Hi, my dear friend.\nType /create to make your profile", reply_markup=get_kb())
    else:
        await message.reply("Hi, my dear friend.", reply_markup=get_kb())
 

@dp.message_handler(commands='create')
async def create_profile(message: types.Message):
    await message.reply('Давайте создадим Ваш профиль!\nДля начала отправьте свой ник/имя')
    await UserState.name.set()


@dp.message_handler(state=UserState.name)
async def create_profile(message: types.Message):
    print(message.text)
    await message.reply('Отлично, теперь отправьте свой возраст.')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def create_profile(message: types.Message):
    print(message.text)
    await message.reply('Отлично, теперь отправьте свое описание.')
    await UserState.description.set()


@dp.message_handler(state=UserState.description)
async def create_profile(message: types.Message):
    print(message.text)
    await message.reply('Профиль создан.')
    await UserState.ended.set()


'''
@dp.message_handler(state=notes.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('Теперь отправьте свой возраст')
    await notes.next()

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer("Команды бота: \n /help \n /create \n /start \n /urls")
'''

if __name__ == '__main__':
    logger.info('Bot started polling.')
    executor.start_polling(dp, skip_updates=True)
