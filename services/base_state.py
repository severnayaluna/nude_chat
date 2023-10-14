class BaseState:

    @classmethod
    @property
    def choices(cls):
        return [
            (cls.__dict__[name])
            for name in cls.__annotations__
            ]