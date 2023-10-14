from services.base_state import BaseState


class State(BaseState):
    a: tuple = (1, 'A')
    b: tuple = (2, 'B')


print(State.choices)