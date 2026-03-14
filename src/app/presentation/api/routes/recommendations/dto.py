from typing import Any

from pydantic import BaseModel, Field

from app.domain.recommendation.value_objects import CompatibilityType


class RecommendationsQuery(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)


class RecommendationResponse(BaseModel):
    ml_recommendation_id: str
    candidate_user_id: str
    score: float
    reason_type: CompatibilityType
    reason_details: dict[str, Any] | None


class RecommendationsResponse(BaseModel):
    items: list[RecommendationResponse]

