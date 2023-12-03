import logging

import os
from typing import Optional

from dotenv import load_dotenv

from log import get_logger

from peewee import Database, SqliteDatabase


logger: logging.Logger = get_logger(__name__)


BASE_DIR: str = os.getcwd().rstrip('/').replace('src', '')

load_dotenv(os.path.join(BASE_DIR, '.env'))
logger.info('Loaded .env.')


BOT_TOKEN: Optional[str] = os.getenv("BOT_TOKEN")
BOT_NAME: str = 'NoNudeBot'


HELP_COMMAND: str = '/help'


MAIN_DB: Database = SqliteDatabase(
    'users.db',
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -32*1000})

TEST_DB: Database = SqliteDatabase(
    'test.db',
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -32*1000})
