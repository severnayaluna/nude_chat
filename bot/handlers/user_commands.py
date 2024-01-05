from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from log import get_logger


logger = get_logger(__name__)


router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.reply(f'Hi, it\'s NoNudeChatRouletteBot.\nType /help to get available commands.')
