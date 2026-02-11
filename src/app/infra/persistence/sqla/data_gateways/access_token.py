from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.access_token.data_gateway import AccessTokenDataGateway
from app.domain.access_token.entity import AccessToken, AccessTokenId
from app.infra.persistence.sqla.tables import access_token_table


class DefaultAccessTokenDataGateway(AccessTokenDataGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def load_with_id(self, access_token_id: AccessTokenId) -> AccessToken | None:
        statement = select(AccessToken).where(
            access_token_table.c.id == access_token_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
