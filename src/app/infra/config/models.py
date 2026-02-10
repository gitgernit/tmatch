from pydantic import BaseModel, ConfigDict, Field


class BaseConfigModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class ServerConfigModel(BaseConfigModel):
    workers: int = Field(default=1, ge=1)
    host: str = Field(default="0.0.0.0")  # noqa: S104
    port: int = Field(default=8080, ge=1, le=65535)
