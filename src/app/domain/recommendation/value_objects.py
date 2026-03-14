from enum import StrEnum
from typing import NewType
from uuid import UUID

RecommendationId = NewType("RecommendationId", UUID)


class CompatibilityType(StrEnum):
    LIFESTYLE = "lifestyle"
