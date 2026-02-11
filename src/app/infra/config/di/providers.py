from dishka import BaseScope, Provider, Scope, provide, provide_all

from app.infra.config.loaders import (
    EnvAccessTokenConfigLoader,
    EnvPostgresConfigLoader,
    EnvServerConfigLoader,
)
from app.infra.config.sources import EnvSource
from app.presentation.api.config.models import AccessTokenConfig, PostgresConfig, ServerConfig


class SourcesProvider(Provider):
    scope: BaseScope | None = Scope.APP

    sources = provide_all(
        EnvSource,
    )


class ConfigProvider(Provider):
    scope: BaseScope | None = Scope.APP

    loaders = provide_all(
        EnvServerConfigLoader,
        EnvPostgresConfigLoader,
        EnvAccessTokenConfigLoader,
    )

    @provide
    def env_server_config(self, loader: EnvServerConfigLoader) -> ServerConfig:
        return loader.load()

    @provide
    def env_postgres_config(self, loader: EnvPostgresConfigLoader) -> PostgresConfig:
        return loader.load()

    @provide
    def env_access_token_config(self, loader: EnvAccessTokenConfigLoader) -> AccessTokenConfig:
        return loader.load()


providers = [
    SourcesProvider(),
    ConfigProvider(),
]
