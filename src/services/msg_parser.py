from aiogram import types

from log import get_logger, log_exceptions


logger = get_logger(__name__)


@log_exceptions(logger)
def parse_content(message: types.Message):
    try:
        ctype = str(message.content_type)
        foo_name = f'send_{ctype}'

        if ctype == 'text':
            return message.text, 'send_message'

        unparsed_content = getattr(message, str(ctype))

        if type(unparsed_content) is not list:
            unparsed_content = [unparsed_content]

        return unparsed_content[-1]['file_id'], foo_name
    except Exception as ex:
        logger.error(ex)
