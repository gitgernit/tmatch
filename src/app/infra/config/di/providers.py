from dishka import BaseScope, Provider, Scope, provide, provide_all

from app.infra.config.loaders import (
    EnvServerConfigLoader,
)
from app.infra.config.sources import EnvSource
from app.presentation.api.config.models import ServerConfig


class SourcesProvider(Provider):
    scope: BaseScope | None = Scope.APP

    sources = provide_all(
        EnvSource,
    )


class ConfigProvider(Provider):
    scope: BaseScope | None = Scope.APP

    loaders = provide_all(
        EnvServerConfigLoader,
    )

    @provide
    def env_server_config(self, loader: EnvServerConfigLoader) -> ServerConfig:
        return loader.load()


providers = [
    SourcesProvider(),
    ConfigProvider(),
]
