import logging

import os

from dotenv import load_dotenv

from templates import templater

from services import query


BASE_DIR = '/home/imcocos/Documents/Director/Git_projects/Nude_Chat/'

logging.basicConfig(
    filename = 'bot.log',
    filemode = 'w',
    level = logging.INFO,
    datefmt = '%m/%d/%Y %I:%M:%S %p')

formatter = logging.Formatter(
    '%(name)s ~$ [ %(levelname)s ](%(asctime)s) - %(message)s')

logger = logging.getLogger()

handler = logging.StreamHandler()
file_handler = logging.FileHandler(
    filename = 'bot.log',
    mode = 'a')

file_handler.setFormatter(formatter)
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(file_handler)


load_dotenv(os.path.join(BASE_DIR, '.env'))
logger.info('Loaded .env.')

BOT_TOKEN=os.getenv("BOT_TOKEN")

BOT_NAME = 'NoNudeBot'

HELP_COMMAND = '/help'

RENDERER = templater.Render()


QUEUE = query.Queue()