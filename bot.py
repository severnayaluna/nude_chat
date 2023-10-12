import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

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

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)


class User_state(StatesGroup):
    name = State()
    age = State()
    des = State()


def get_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))
    kb.add(KeyboardButton('/help'))
    return kb


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Hi, my dear friend", reply_markup=get_kb())
    await message.reply("Уведомления включены")
 
'''
@dp.message_handler(commands='create')
async def cmd_create(message: types.Message):
    await message.reply('Давайте создадим Ваш профиль!\nДля начала отправьте фотографию')
    await notes.photo.set()


@dp.message_handler(state=notes.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('Теперь отправьте свой возраст')
    await notes.next()
'''
 
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer("Команды бота: \n /help \n /create \n /start \n /urls")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
