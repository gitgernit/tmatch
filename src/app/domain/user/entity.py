from datetime import UTC, datetime
from typing import NewType, Self
from uuid import UUID

from uuid_utils.compat import uuid7

from app.domain.common.entity import Entity, entity

UserId = NewType("UserId", UUID)


@entity
class User(Entity[UserId]):
    @classmethod
    def factory(cls) -> Self:
        return cls(
            id=UserId(uuid7()),
            created_at=datetime.now(tz=UTC),
        )
