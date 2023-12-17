"""
Exceptions
"""
from services.exceptions import MyBaseException, UserIsBot


try:
    raise UserIsBot
except MyBaseException:
    print('Handled')
finally:
    print('Not handled')
