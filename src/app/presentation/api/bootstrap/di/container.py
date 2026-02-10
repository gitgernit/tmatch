from dishka import STRICT_VALIDATION, AsyncContainer, make_async_container

from app.infra.config.di.providers import providers as config_providers


def build_container() -> AsyncContainer:
    return make_async_container(
        *config_providers,
        validation_settings=STRICT_VALIDATION,
    )
