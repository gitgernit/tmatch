from app.application.common.dto import dto
from app.domain.recommendation.value_objects import CompatibilityType


@dto
class RecommendationReasonItem:
    score: float
    reason_type: CompatibilityType


@dto
class RecommendationItem:
    ml_recommendation_id: str
    candidate_user_id: str
    reasons: list[RecommendationReasonItem]


@dto
class RecommendationsResult:
    items: list[RecommendationItem]
