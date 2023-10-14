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
    '%(name)s ~$ [ %(levelname)s ](%(asctime)s) - %(message)s')

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


def get_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))
    kb.add(KeyboardButton('/help'))
    return kb


bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)
logger.info('Bot and dp was created.')


'''
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):

    if not UserState.ended:
        await message.reply("Приветствую, дорогой друг \nНажми /create для создания профиля", reply_markup=get_kb())
    else:
        await message.reply("Приветствую, дорогой друг", reply_markup=get_kb())
 

@dp.message_handler(commands='create')
async def create_profile(message: types.Message):
    user, exists = User.get_or_create_by_msg(message)
    exists = not exists
    logger.info(f'User {user.tgid} exists: {exists}!')
    if exists:
        if user.reg:
            await UserState.ended.set()
            await message.reply('Ваш профиль уже создан!')
            return
        if user.name:
            await UserState.age.set()
            logger.info(f'User {user.tgid} age!')
            return
        if user.age:
            await UserState.description.set()
            logger.info(f'User {user.tgid} desc!')
            return

    await message.reply(f'Давайте создадим Ваш профиль!\nДля начала отправьте свое имя')
    await UserState.name.set()
    logger.info(f'User {user.tgid} name!')


@dp.message_handler(state=UserState.name)
async def create_profile(message: types.Message):
    user: User = User.get_by_msg(message)


    error = user.set_name(message.text)
    if error:
        await message.reply(f'Ошибка в имени - {error}')   
        return
 
    await message.reply('Отправьте свой возраст.')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def create_profile(message: types.Message):
    user: User = User.get_by_msg(message)


    error = user.set_age(message.text)
    if error:
        await message.reply(f'Ошибка в возрасте - {error}')   
        return
 
    await message.reply('Теперь отправьте описание.')
    await UserState.description.set()


@dp.message_handler(state=UserState.description)
async def description_setting(message: types.Message):
    logger.warning('Entering desc func')
    user: User = User.get_by_msg(message)
    logger.warning('Got user')
    user.set_description(message.text)
    logger.warning('Setted desc')
    await message.reply('Профиль создан.')
    user.reg = True
    logger.warning('User.reg set to True')
    user.save()
    logger.warning('User.save()')
    await UserState.ended.set()
    logger.warning('State set to ended')


@dp.message_handler(commands=['profile'])
async def profile(message: types.Message):
    user, exists = User.get_or_create_by_msg(message)
    print(user, exists)
    if not user.reg:
        await message.reply(f'Профиль еще не создан!')
        return

    await message.reply(f'Ваш профиль:\n\
    Имя: {user.name}\n\
    Возраст: {user.age}\n\
    О себе: {user.description}\n\
    ')


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer("Команды бота: \n /help \n /create \n /start \n /urls")

'''


@dp.message_handler(commands=['set_ended'])
async def set_ended(message: types.Message):
    user, exists = User.get_or_create_by_msg(message)
    user: User
    user.state = User.State.ended
    user.save()
    await message.reply(f'State is {user.state}')


@dp.message_handler(User.state_is_ended)
async def only_ended(message: types.Message):
    await message.reply('Ended')



if __name__ == '__main__':
    logger.info('Bot started polling.')
    executor.start_polling(dp, skip_updates=False)
