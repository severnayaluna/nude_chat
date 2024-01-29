from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import Table

from bot.core.db.models import user

from bot.log import get_logger

logger = get_logger(__name__)


class User:
    async def __init__(self, id_: int | str, db: AsyncEngine) -> None:
        async with db.begin() as connection:
            db_user = await connection.execute(
                user.select().where(user.c.id == int(id_))
            )
            if not db_user:
                db_user = await connection.execute(
                    user.insert(), [{"id": id_}]
                )
        self.unpack(db_user)

    def unpack(self, db_user: Table) -> None:
        try:
            for field_name in user.c.keys():
                setattr(self, field_name, getattr(db_user, field_name))
        except Exception as ex:
            logger.error(ex)
