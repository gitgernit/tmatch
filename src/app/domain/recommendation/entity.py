from datetime import UTC, datetime
from typing import Any, Self

from uuid_utils.compat import uuid7

from app.domain.common.entity import Entity, entity
from app.domain.recommendation.value_objects import CompatibilityType, RecommendationId
from app.domain.user.entity import UserId


@entity
class Recommendation(Entity[RecommendationId]):
    user_id: UserId
    candidate_user_id: UserId
    score: float
    reason_type: CompatibilityType
    reason_details: dict[str, Any] | None

    @classmethod
    def factory(
        cls,
        user_id: UserId,
        candidate_user_id: UserId,
        score: float,
        reason_type: CompatibilityType,
        reason_details: dict[str, Any] | None = None,
    ) -> Self:
        return cls(
            id=RecommendationId(uuid7()),
            created_at=datetime.now(tz=UTC),
            user_id=user_id,
            candidate_user_id=candidate_user_id,
            score=score,
            reason_type=reason_type,
            reason_details=reason_details,
        )
