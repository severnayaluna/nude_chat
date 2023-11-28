from aiogram import types


def parse_content(message: types.Message):
    ctype = str(message.content_type)
    foo_name = f'send_{ctype}'

    if ctype == 'text':
        return message.text, 'send_message'

    unparsed_content = getattr(message, str(ctype))
    
    if type(unparsed_content) is not list:
        unparsed_content = [unparsed_content]

    return unparsed_content[-1]['file_id'], foo_name
