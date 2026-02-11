from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.user.data_gateway import UserDataGateway
from app.domain.user.entity import User, UserId
from app.infra.persistence.sqla.tables import user_table


class DefaultUserDataGateway(UserDataGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def load_with_id(self, user_id: UserId) -> User | None:
        statement = select(User).where(user_table.c.id == user_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
