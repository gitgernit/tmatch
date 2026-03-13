from datetime import date

from pydantic import BaseModel, Field


class UpsertProfileRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=80)
    last_name: str | None = Field(None, min_length=1, max_length=80)
    birth_date: date
    region: str | None = Field(None, min_length=1, max_length=120)
    avatar_url: str | None = Field(None, max_length=2048)


class ProfileResponse(BaseModel):
    user_id: str
    first_name: str
    last_name: str | None
    birth_date: date
    region: str | None
    avatar_url: str | None
