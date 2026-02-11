from typing import Final

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, MetaData, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

from app.domain.access_token.entity import AccessToken
from app.domain.user.entity import User

meta_data: Final = MetaData()
mapper_registry: Final = registry()

user_table: Final = Table(
    "users",
    meta_data,
    Column("id", UUID, primary_key=True),
    Column("deleted_at", DateTime(timezone=True)),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

access_token_table: Final = Table(
    "access_token",
    meta_data,
    Column("id", UUID, primary_key=True),
    Column("user_id", UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("revoked", Boolean, nullable=False),
    Column("expires_in", DateTime(timezone=True), nullable=False),
    Column("deleted_at", DateTime(timezone=True)),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

mapper_registry.map_imperatively(User, user_table)
mapper_registry.map_imperatively(AccessToken, access_token_table)
