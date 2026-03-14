from enum import StrEnum
from typing import NewType
from uuid import UUID

from app.domain.common.value_object import value_object

RecommendationId = NewType("RecommendationId", UUID)


class CompatibilityType(StrEnum):
    LIFESTYLE = "lifestyle"


@value_object
class RecommendationReason:
    score: float
    reason_type: CompatibilityType
