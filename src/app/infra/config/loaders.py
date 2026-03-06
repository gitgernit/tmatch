from adaptix import Retort

from app.infra.config.models import (
    AccessTokenConfigModel,
    PostgresConfigModel,
    ServerConfigModel,
    YandexOAuthConfigModel,
)
from app.infra.config.sources import EnvSource
from app.presentation.api.config.models import (
    AccessTokenConfig,
    PostgresConfig,
    ServerConfig,
    YandexOAuthConfig,
)

retort = Retort()


class BaseEnvLoader:
    def __init__(self, source: EnvSource) -> None:
        self._source = source


class EnvServerConfigLoader(BaseEnvLoader):
    def load(self) -> ServerConfig:
        raw_data = self._source.get_present_values(["SERVER_WORKERS", "SERVER_HOST", "SERVER_PORT"])
        validated = ServerConfigModel.model_validate(raw_data).model_dump()

        return retort.load(validated, ServerConfig)


class EnvPostgresConfigLoader(BaseEnvLoader):
    def load(self) -> PostgresConfig:
        raw_data = self._source.get_present_values(
            ["POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB"]
        )
        validated = PostgresConfigModel.model_validate(raw_data).model_dump()

        return retort.load(validated, PostgresConfig)


class EnvAccessTokenConfigLoader(BaseEnvLoader):
    def load(self) -> AccessTokenConfig:
        raw_data = self._source.get_present_values(["ACCESS_TOKEN_CRYPTO_KEY", "ACCESS_TOKEN_EXPIRES_IN_SECONDS"])
        validated = AccessTokenConfigModel.model_validate(raw_data).model_dump()

        return retort.load(validated, AccessTokenConfig)


class EnvYandexOAuthConfigLoader(BaseEnvLoader):
    def load(self) -> YandexOAuthConfig:
        raw_data = self._source.get_present_values(["YANDEX_OAUTH_CLIENT_ID", "YANDEX_OAUTH_CLIENT_SECRET"])
        validated = YandexOAuthConfigModel.model_validate(raw_data).model_dump()

        return retort.load(validated, YandexOAuthConfig)
