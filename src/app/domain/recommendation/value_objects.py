from enum import StrEnum
from typing import NewType
from uuid import UUID

from app.domain.common.value_object import value_object

RecommendationId = NewType("RecommendationId", UUID)


class RecommendationFeatureName(StrEnum):
    LIFESTYLE = "lifestyle"


@value_object
class RecommendationReason:
    feature_name: RecommendationFeatureName
    score: float
