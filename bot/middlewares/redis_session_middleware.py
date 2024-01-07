"""
Unneeded middleware - do not use it,
instead - use DI via dp
"""
from typing import Callable, Awaitable, Any, Dict

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject



class RedisSessionMeddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        print('Before')
        data['redis_storage'] = data['dispatcher']['redis_storage']
        print('After')
        return await handler(event, data)
