import logging

import os

from dotenv import load_dotenv


BASE_DIR = os.getcwd().rstrip('/').replace('src', '')

logging.basicConfig(
    filename = 'bot.log',
    filemode = 'a',
    level = logging.INFO,
    datefmt = '%m/%d/%Y %I:%M:%S %p')


logger = logging.Logger(__name__, level=logging.INFO)

formatter = logging.Formatter(
    '%(name)s ~$ [ %(levelname)s ](%(asctime)s) - %(message)s')

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(
    filename = 'bot.log',
    mode = 'a')

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


load_dotenv(os.path.join(BASE_DIR, '.env'))
logger.info('Loaded .env.')

BOT_TOKEN=os.getenv("BOT_TOKEN")

BOT_NAME = 'NoNudeBot'

HELP_COMMAND = '/help'
