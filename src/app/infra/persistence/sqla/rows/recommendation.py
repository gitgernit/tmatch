from datetime import datetime
from typing import Any
from uuid import UUID

from app.domain.recommendation.value_objects import CompatibilityType


class RecommendationRow:
    id: UUID | None
    user_id: UUID | None
    candidate_user_id: UUID | None
    score: float | None
    reason_type: CompatibilityType | None
    reason_details: dict[str, Any] | None
    created_at: datetime | None

    def __init__(
        self,
        id_: UUID | None = None,
        user_id: UUID | None = None,
        candidate_user_id: UUID | None = None,
        score: float | None = None,
        reason_type: CompatibilityType | None = None,
        reason_details: dict[str, Any] | None = None,
        created_at: datetime | None = None,
    ) -> None:
        self.id = id_
        self.user_id = user_id
        self.candidate_user_id = candidate_user_id
        self.score = score
        self.reason_type = reason_type
        self.reason_details = reason_details
        self.created_at = created_at
