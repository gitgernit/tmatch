from typing import override

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dating_profile.data_gateway import DatingProfileDataGateway
from app.domain.dating_profile.entity import DatingProfile
from app.domain.dating_profile.value_objects import DatingProfileId
from app.domain.user.entity import UserId
from app.infra.persistence.sqla.mappers.dating_profile_mapper import DatingProfileMapper
from app.infra.persistence.sqla.rows import (
    DatingProfilePhotoRow,
    DatingProfileRow,
    DatingProfileTraitRow,
)
from app.infra.persistence.sqla.tables import (
    dating_profile_photo_table,
    dating_profile_table,
    dating_profile_trait_table,
)


class DefaultDatingProfileDataGateway(DatingProfileDataGateway):
    def __init__(
        self,
        session: AsyncSession,
        dating_profile_mapper: DatingProfileMapper,
    ) -> None:
        self._session = session
        self._mapper = dating_profile_mapper

    @override
    async def load_by_user_id(self, user_id: UserId) -> DatingProfile | None:
        result = await self._session.execute(
            select(DatingProfileRow).where(dating_profile_table.c.user_id == user_id),
        )
        profile_row = result.scalar_one_or_none()
        if profile_row is None:
            return None
        if profile_row.id is None:
            return None
        photos_result = await self._session.execute(
            select(DatingProfilePhotoRow).where(
                dating_profile_photo_table.c.dating_profile_id == profile_row.id,
            ),
        )
        photo_rows = list(photos_result.scalars().all())
        traits_result = await self._session.execute(
            select(DatingProfileTraitRow).where(
                dating_profile_trait_table.c.dating_profile_id == profile_row.id,
            ),
        )
        trait_rows = list(traits_result.scalars().all())
        return self._mapper.to_entity(profile_row, photo_rows, trait_rows)

    @override
    async def delete_photos_by_dating_profile_id(
        self,
        dating_profile_id: DatingProfileId,
    ) -> None:
        await self._session.execute(
            delete(dating_profile_photo_table).where(
                dating_profile_photo_table.c.dating_profile_id == dating_profile_id,
            ),
        )

    @override
    async def set_trait_hidden(
        self,
        dating_profile_id: DatingProfileId,
        trait_code: str,
        *,
        is_hidden: bool,
    ) -> None:
        await self._session.execute(
            update(dating_profile_trait_table)
            .where(
                dating_profile_trait_table.c.dating_profile_id == dating_profile_id,
                dating_profile_trait_table.c.trait_code == trait_code,
            )
            .values(is_hidden=is_hidden),
        )
