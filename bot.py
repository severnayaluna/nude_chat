import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from models import User, Room
from services.decorators import my_msg_handler

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

'''
# Тестовые функции
async def err(message: types.Message, something):
    await message.reply('Not age: ' + str(something))

@my_msg_handler(
    dp,
    commands=['some'],
    state=User.State.ended,
    err_callback=err,
    something='some text')
async def some(message):
    await message.reply('Some')
'''

@my_msg_handler(dp, commands=['start'], send_user=True)
async def cmd_start(message: types.Message, user: User, exists: bool):
    """Старт функция.

    Args:
        message (types.Message): сообщение пользователя
        user (User): юзер который передается @my_msg_handler
        exists (bool): сущетсвовал ли юзер до вызова функции
    """    
    if not user.reg_state == User.RegState.ended:
        await message.reply("Приветствую, дорогой друг \nНажми /create для создания профиля", reply_markup=get_kb())
    else:
        await message.reply("Приветствую, дорогой друг", reply_markup=get_kb())
 


@my_msg_handler(dp, commands=['create'], send_user=True)
async def create_profile(message: types.Message, user: User, exists: bool):
    """Функция создания пользователя.
    Ветвление по стэйтам.

    Args:
        message (types.Message): сообщение пользователя
        user (User): юзер который передается @my_msg_handler
        exists (bool): сущетсвовал ли юзер до вызова функции
    """    
    logger.info(f'User {user.tgid} exists: {exists}!')
    if exists:
        if user.reg:
            user.set_state('reg_state', User.RegState.ended)
            await message.reply('Ваш профиль уже создан!')
            return
        if user.name:
            user.set_state('reg_state', User.RegState.age)
            logger.info(f'User {user.tgid} age!')
            return
        if user.age:
            user.set_state('reg_state', User.RegState.description)
            logger.info(f'User {user.tgid} desc!')
            return

    await message.reply(f'Давайте создадим Ваш профиль!\nДля начала отправьте свое имя')
    user.set_state('reg_state', User.RegState.name)
    logger.info(f'User {user.tgid} name!')

@state_requiered(reg_state=User.RegState.ended, find_state=User.FindState.waiting, filter=all)
@my_msg_handler(dp, state=User.State.name, send_user=True)
async def create_profile(message: types.Message, user: User, exists: bool):
    """Функция создания профиля юзера. Требует нэйм-стэйт

    Args:
        message (types.Message): сообщение пользователя
        user (User): юзер который передается @my_msg_handler
        exists (bool): сущетсвовал ли юзер до вызова функции
    """    
    error = user.set_name(message.text)
    if error:
        await message.reply(f'Ошибка в имени - {error}')   
        return
 
    user.set_state(User.State.age)
    await message.reply('Отправьте свой возраст.')


@my_msg_handler(dp, state=User.State.age, send_user=True)
async def create_profile(message: types.Message, user: User, exists: bool):
    """Функция создания профиля юзера. Требует эйдж-стэйт

    Args:
        message (types.Message): сообщение пользователя
        user (User): юзер который передается @my_msg_handler
        exists (bool): сущетсвовал ли юзер до вызова функции
    """    
    error = user.set_age(message.text)
    if error:
        await message.reply(f'Ошибка в возрасте - {error}')   
        return
 
    user.set_state(User.State.description)
    await message.reply('Теперь отправьте описание.')


@my_msg_handler(dp, state=User.State.description, send_user=True)
async def create_profile(message: types.Message, user: User, exists: bool):
    """Функция создания профиля юзера. Требует дескрипшн-стэйт

    Args:
        message (types.Message): сообщение пользователя
        user (User): юзер который передается @my_msg_handler
        exists (bool): сущетсвовал ли юзер до вызова функции
    """    
    user.set_description(message.text)
    user.set_reg(True)
    user.set_state(User.State.ended)
    await message.reply('Профиль создан.')


async def profile_not_reg_error(message: types.Message):
    """Вывод ошибки отсутствия профиля.

    Args:
        message (types.Message): сообщение пользователя
    """    
    await message.reply(f'Профиль еще не создан!')


@my_msg_handler(
    dp,
    commands=['profile'],
    state=User.State.ended,
    err_callback=profile_not_reg_error,
    send_user=True)
async def send_profile(message: types.Message, user: User, exists: bool):
    """Функция вывода профиля.
    При отсутствии полного профиля зовет profile_not_reg_error.

    Args:
        message (types.Message): сообщение пользователя
        user (User): юзер который передается @my_msg_handler
        exists (bool): сущетсвовал ли юзер до вызова функции
    """    
    await message.reply(f'Ваш профиль:\n\
    Имя: {user.name}\n\
    Возраст: {user.age}\n\
    О себе: {user.description}\n\
    ')


@my_msg_handler(dp, commands=['help'])
async def cmd_help(message: types.Message):
    """Функция вывода комманд.

    Args:
        message (types.Message): сообщение пользователя
    """    
    await message.answer(
        "Команды бота:\n\
            /help - Комманды бота\n\
            /create - Создание профиля\n\
            /start - Старт\n\
            /profile - Вывод профиля")


if __name__ == '__main__':
    logger.info('Bot started polling.')
    executor.start_polling(dp, skip_updates=True)
