from datetime import UTC, datetime
from typing import Self

from uuid_utils.compat import uuid7

from app.domain.common.entity import Entity, entity
from app.domain.interaction.value_objects import InteractionId, InteractionType
from app.domain.user.entity import UserId


@entity
class Interaction(Entity[InteractionId]):
    actor_user_id: UserId
    candidate_user_id: UserId
    action: InteractionType

    @classmethod
    def factory(
        cls,
        actor_user_id: UserId,
        candidate_user_id: UserId,
        action: InteractionType,
    ) -> Self:
        return cls(
            id=InteractionId(uuid7()),
            created_at=datetime.now(tz=UTC),
            actor_user_id=actor_user_id,
            candidate_user_id=candidate_user_id,
            action=action,
        )
