from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class CreateInteractionRequest(BaseModel):
    candidate_user_id: UUID
    action: Literal["like", "dislike"] = Field(...)
    ml_recommendation_id: str | None = Field(None, max_length=256)


class InteractionResponse(BaseModel):
    interaction_id: UUID
    actor_user_id: UUID
    candidate_user_id: UUID
    action: Literal["like", "dislike"]
    created_at: datetime
    ml_recommendation_id: str | None = None
