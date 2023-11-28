from models import User
from services.custom_state.base_state import State

user: User = User.create(tgid=1222222)
user = User.get(id=1)
print(user.reg_state)

us: User = User.get_or_create(tgid=1)[0]


us.set_state('reg_state', User.RegState.name)

print(us.get_state('reg_state'))

als = User.RegState.choices
print(als)
us_state = us.get_state('reg_state')
acs = ~State('find') & ~State('name')
print(us_state.state)
print(acs.is_state_acessed(us_state))
