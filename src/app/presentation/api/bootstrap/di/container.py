from dishka import STRICT_VALIDATION, AsyncContainer, make_async_container
from dishka.integrations.litestar import LitestarProvider

from app.infra.config.di.providers import providers as config_providers
from app.infra.persistence.sqla.di.providers import providers as sqla_providers
from app.infra.security.di.providers import providers as security_providers


def build_container() -> AsyncContainer:
    return make_async_container(
        LitestarProvider(),
        *config_providers,
        *sqla_providers,
        *security_providers,
        validation_settings=STRICT_VALIDATION,
    )
