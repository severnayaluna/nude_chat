from models import User

user: User = User.create(tgid=1222222)
user = User.get(id=1)
print(user.reg_state)

user.set_state('reg_state', User.RegState.ended)

print(user.reg_state)
