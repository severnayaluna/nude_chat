def handle_exceptions(logger):
    def decorator(foo: callable):
        async def wrapper(*args, **_):
            try:
                return await foo(*args)
            except Exception as ex:
                logger.error(ex)
                json_ex = ex.json()
                await args[0].reply(
                    f'Error - {json_ex["name"]}:\n{json_ex["text"]}'
                )
        return wrapper
    return decorator


class MyBaseException(Exception):
    def json(self: Exception):
        return {
            'name': self.__class__.__name__,
            'text': self.args[0],
        }
    
    def log_me(self, logger):
        logger.error(self)


class NoPairsInQueue(MyBaseException):
    ...


class DuplicateUser(MyBaseException):
    ...


class NoSuchUser(MyBaseException):
    ...


class UserIsBot(MyBaseException):
    ...


class WrongType(MyBaseException):
    ...

class UnboundError(MyBaseException):
    ...

class SameUserError(MyBaseException):
    ...
