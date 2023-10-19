class Logic:
    def __and__(self, other):
        st: Condition = Condition()
        st.is_state_acessed: callable = lambda state:\
            self.is_state_acessed(state) and (other.is_state_acessed(state) if hasattr(other, 'is_state_acessed') else bool(other))
        return st
    
    def __or__(self, other):
        st: Condition = Condition()
        st.is_state_acessed: callable = lambda state:\
            self.is_state_acessed(state) or (other.is_state_acessed(state) if hasattr(other, 'is_state_acessed') else bool(other))
        return st
    
    def __invert__(self):
        st: Condition = Condition()
        st.is_state_acessed: callable = lambda state:\
            not(self.is_state_acessed(state))
        return st


class Condition(Logic):
    def __init__(self):
        self.is_state_acessed: callable = lambda state: state.state == self.state


class State(Logic):
    def __init__(self, state_name):
        self.state = state_name
        self.is_state_acessed: callable = lambda state: state.state == self.state


class BaseState:
    """
    Базовый стэйт
    """    
    @classmethod
    @property
    def choices(cls):
        """Функция возвращающая все аннотированные стэйты из дочернего класса.

        Returns:
            list: лист аннотированных стэйтов
        """        
        return [
            (cls.__dict__[name])
            for name in cls.__annotations__
            ]
