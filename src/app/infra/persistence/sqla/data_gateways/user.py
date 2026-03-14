from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.user.data_gateway import UserDataGateway
from app.domain.user.entity import User, UserId
from app.infra.persistence.sqla.mappers.user_mapper import UserMapper
from app.infra.persistence.sqla.rows import ProfileRow, UserRow
from app.infra.persistence.sqla.tables import profile_table, user_table


class DefaultUserDataGateway(UserDataGateway):
    def __init__(self, session: AsyncSession, user_mapper: UserMapper) -> None:
        self._session = session
        self._user_mapper = user_mapper

    @override
    async def load_with_id(self, user_id: UserId) -> User | None:
        user_result = await self._session.execute(
            select(UserRow).where(user_table.c.id == user_id),
        )
        user_row = user_result.scalar_one_or_none()
        if user_row is None:
            return None
        profile_result = await self._session.execute(
            select(ProfileRow).where(profile_table.c.user_id == user_id),
        )
        profile_row = profile_result.scalar_one_or_none()
        return self._user_mapper.to_entity(user_row, profile_row)

    @override
    async def list_user_ids(
        self,
        limit: int,
        exclude_user_id: UserId | None = None,
    ) -> list[UserId]:
        stmt = select(user_table.c.id).order_by(user_table.c.id).limit(limit)
        if exclude_user_id is not None:
            stmt = stmt.where(user_table.c.id != exclude_user_id)
        result = await self._session.execute(stmt)
        return [UserId(row[0]) for row in result.all()]
