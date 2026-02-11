from pydantic import BaseModel, ConfigDict, Field


class BaseConfigModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class ServerConfigModel(BaseConfigModel):
    workers: int = Field(default=1, ge=1, alias="SERVER_WORKERS")
    host: str = Field(default="0.0.0.0", alias="SERVER_HOST")  # noqa: S104
    port: int = Field(default=8080, ge=1, le=65535, alias="SERVER_PORT")


class PostgresConfigModel(BaseConfigModel):
    host: str = Field(default="localhost", alias="POSTGRES_HOST")
    port: int = Field(default=5432, ge=1, le=65535, alias="POSTGRES_PORT")
    user: str = Field(default="postgres", alias="POSTGRES_USER")
    password: str = Field(default="", alias="POSTGRES_PASSWORD")
    db: str = Field(default="app", alias="POSTGRES_DB")


class AccessTokenConfigModel(BaseConfigModel):
    crypto_key: str = Field(default="AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=", alias="ACCESS_TOKEN_CRYPTO_KEY")
    expires_in_seconds: int = Field(default=86400, ge=1, alias="ACCESS_TOKEN_EXPIRES_IN_SECONDS")
