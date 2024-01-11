from typing import Callable, Awaitable, Any, Dict, Iterable

from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Message



class AcessMiddleware(BaseMiddleware):
    def __init__(self, ids: int | Iterable[int]) -> None:
        self.ids: Iterable[int]
        if isinstance(ids, int):
            self.ids = [ids]
        else:
            self.ids = ids

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject | Message,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)
        if not event.from_user:
            return await handler(event, data)
        if event.from_user.id in self.ids:
            return await handler(event, data)
