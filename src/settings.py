import os

from dotenv import load_dotenv

from log import get_logger

from peewee import SqliteDatabase


logger = get_logger(__name__)


BASE_DIR = os.getcwd().rstrip('/').replace('src', '')

load_dotenv(os.path.join(BASE_DIR, '.env'))
logger.info('Loaded .env.')


BOT_TOKEN=os.getenv("BOT_TOKEN")
BOT_NAME = 'NoNudeBot'


HELP_COMMAND = '/help'


MAIN_DB = SqliteDatabase(
    'users.db',
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -32*1000})

TEST_DB = SqliteDatabase(
    'test.db',
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -32*1000})
