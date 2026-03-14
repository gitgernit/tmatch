from typing import Final

from sqlalchemy import Boolean, Column, Date, DateTime, Enum, ForeignKey, MetaData, String, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry

from app.domain.auth_identity.value_objects import AuthMethod
from app.infra.persistence.sqla.rows import (
    AccessTokenRow,
    AuthIdentityRow,
    NotificationDeviceRow,
    ProfileRow,
    UserRow,
)

meta_data: Final = MetaData()
mapper_registry: Final = registry()

user_table: Final = Table(
    "users",
    meta_data,
    Column("id", UUID, primary_key=True),
    Column("deleted_at", DateTime(timezone=True)),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

profile_table: Final = Table(
    "profiles",
    meta_data,
    Column("user_id", UUID, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=True),
    Column("birth_date", Date, nullable=False),
    Column("region", String, nullable=True),
    Column("avatar_url", String, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=True),
)

auth_identity_table: Final = Table(
    "auth_identities",
    meta_data,
    Column("id", UUID, primary_key=True),
    Column("user_id", UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("method", Enum(AuthMethod, name="auth_method"), nullable=False),
    Column("identifier", String, nullable=False),
    Column("secret_key", String, nullable=True),
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

notification_device_table: Final = Table(
    "notification_devices",
    meta_data,
    Column("id", UUID, primary_key=True),
    Column("user_id", UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("device_id", String, nullable=False),
    Column("deleted_at", DateTime(timezone=True)),
    Column("created_at", DateTime(timezone=True), nullable=False),
    UniqueConstraint("user_id", "device_id", name="uq_notification_devices_user_device"),
)

mapper_registry.map_imperatively(UserRow, user_table)
mapper_registry.map_imperatively(ProfileRow, profile_table)
mapper_registry.map_imperatively(AuthIdentityRow, auth_identity_table)
mapper_registry.map_imperatively(AccessTokenRow, access_token_table)
mapper_registry.map_imperatively(NotificationDeviceRow, notification_device_table)
