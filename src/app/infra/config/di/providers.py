from dishka import BaseScope, Provider, Scope, provide, provide_all

from app.infra.config.loaders import (
    EnvAccessTokenConfigLoader,
    EnvFirebaseConfigLoader,
    EnvOpentelemetryConfigLoader,
    EnvPostgresConfigLoader,
    EnvServerConfigLoader,
    EnvYandexOAuthConfigLoader,
)
from app.infra.config.sources import EnvSource
from app.presentation.api.config.models import (
    AccessTokenConfig,
    FirebaseConfig,
    OpentelemetryConfig,
    PostgresConfig,
    ServerConfig,
    YandexOAuthConfig,
)


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
        EnvYandexOAuthConfigLoader,
        EnvOpentelemetryConfigLoader,
        EnvFirebaseConfigLoader,
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

    @provide
    def env_yandex_oauth_config(self, loader: EnvYandexOAuthConfigLoader) -> YandexOAuthConfig:
        return loader.load()

    @provide
    def env_opentelemetry_config(
        self, loader: EnvOpentelemetryConfigLoader
    ) -> OpentelemetryConfig:
        return loader.load()

    @provide
    def env_firebase_config(self, loader: EnvFirebaseConfigLoader) -> FirebaseConfig:
        return loader.load()


providers = [
    SourcesProvider(),
    ConfigProvider(),
]
