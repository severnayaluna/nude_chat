# install aiogram, datetime, asyncio, pytz, requests, bs4
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from models import User, Room

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6594691217:AAE-sYGH2hLdkCALx09-qHWcoYSPM3JqYME")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


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

@dp.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 120, state=notes.age)
async def check_age(message: types.Message):
    await message.reply('Введите реальный возраст числом')

@dp.message_handler(state=notes.age)
async def load_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    await message.reply('а теперь расскажите немного о себе')
    await notes.next()

@dp.message_handler(state=notes.des)
async def load_des(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['des'] = message.text
    tz_moscow = pytz.timezone('Europe/Moscow')
    now = datetime.now(tz_moscow)
    ct = now.strftime("%H:%M:%S")
    await bot.send_photo(chat_id=message.from_user.id, photo=data['photo'], caption=f"{data['name']}, {data['age']}\n {data['des']} \n Московское время: {ct}")

    await message.answer('Ваша анкета успешно создана')
    await state.finish()

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer("Команды бота: \n /help \n /create \n /start \n /urls")

@dp.message_handler()
async def echo_message(msg: types.Message):
        await bot.send_message(msg.from_user.id, msg.text)
        await bot.send_message(msg.from_user.id,  text="Это не команда бота")

async def on_startup(dp): 
    await bot.send_message( 696941814, '!WARNING! Бот был запущен !WARNING!')

async def on_shutdown(dp): 
    await bot.send_message( 696941814, '!WARNING! Бот был убит !WARNING!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup, on_shutdown=on_shutdown)