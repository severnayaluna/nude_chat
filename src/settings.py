import os

from dotenv import load_dotenv

from log import get_logger

logger = get_logger(__name__)

BASE_DIR = os.getcwd().rstrip('/').replace('src', '')

load_dotenv(os.path.join(BASE_DIR, '.env'))
logger.info('Loaded .env.')

BOT_TOKEN=os.getenv("BOT_TOKEN")

BOT_NAME = 'NoNudeBot'

HELP_COMMAND = '/help'
