from models import *

def get_user(message):
    user: User = User.get(tgid=message.from_user.id)
    return user