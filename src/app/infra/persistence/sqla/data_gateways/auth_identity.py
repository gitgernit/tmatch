from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.auth_identity.data_gateway import AuthIdentityDataGateway
from app.domain.auth_identity.entity import AuthIdentity
from app.domain.auth_identity.value_objects import AuthMethod
from app.infra.persistence.sqla.tables import auth_identity_table


class DefaultAuthIdentityDataGateway(AuthIdentityDataGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def load_by_method_and_identifier(
        self,
        method: AuthMethod,
        identifier: str,
    ) -> AuthIdentity | None:
        statement = select(AuthIdentity).where(
            auth_identity_table.c.method == method,
            auth_identity_table.c.identifier == identifier,
            auth_identity_table.c.deleted_at.is_(None),
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
