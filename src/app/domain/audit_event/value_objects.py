from enum import StrEnum
from typing import NewType
from uuid import UUID

AuditEventId = NewType("AuditEventId", UUID)


class AuditEventType(StrEnum):
    INTERACTION_CREATED = "interaction.created"
    RECOMMENDATION_SHOWN = "recommendation.shown"
    PROFILE_UPDATED = "profile.updated"
