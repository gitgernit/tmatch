from typing import Any

from app.application.common.dto import dto
from app.domain.recommendation.value_objects import CompatibilityType


@dto
class RecommendationItem:
    ml_recommendation_id: str
    candidate_user_id: str
    score: float
    reason_type: CompatibilityType
    reason_details: dict[str, Any] | None


@dto
class RecommendationsResult:
    items: list[RecommendationItem]

