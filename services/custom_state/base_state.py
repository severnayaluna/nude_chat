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
