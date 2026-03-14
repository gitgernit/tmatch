from typing import Any, override

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.common.unit_of_work import UnitOfWork
from app.domain.common.entity import Entity
from app.infra.persistence.sqla.mappers import GlobalDataMapper


class DefaultUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession, data_mapper: GlobalDataMapper) -> None:
        self._session = session
        self._data_mapper = data_mapper
        self._pending: list[Entity[Any]] = []

    @override
    async def add(self, *entities: Entity[Any]) -> None:
        self._pending.extend(entities)

    @override
    async def commit(self) -> None:
        for entity in self._pending:
            for row in self._data_mapper.to_rows(entity):
                self._session.merge(row)
        self._pending.clear()
        await self._session.commit()
