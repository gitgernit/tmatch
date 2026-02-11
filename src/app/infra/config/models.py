from pydantic import BaseModel, ConfigDict, Field


class BaseConfigModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class ServerConfigModel(BaseConfigModel):
    workers: int = Field(default=1, ge=1)
    host: str = Field(default="0.0.0.0")  # noqa: S104
    port: int = Field(default=8080, ge=1, le=65535)


class PostgresConfigModel(BaseConfigModel):
    host: str = Field(default="localhost", alias="POSTGRES_HOST")
    port: int = Field(default=5432, ge=1, le=65535, alias="POSTGRES_PORT")
    user: str = Field(default="postgres", alias="POSTGRES_USER")
    password: str = Field(default="", alias="POSTGRES_PASSWORD")
    db: str = Field(default="app", alias="POSTGRES_DB")
