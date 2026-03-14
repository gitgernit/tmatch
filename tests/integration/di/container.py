from dishka import STRICT_VALIDATION, AsyncContainer, BaseScope, Provider, Scope, make_async_container, provide

from app.application.auth_identity.di.providers import providers as auth_identity_providers
from app.application.common.identity_provider import IdentityProvider
from app.application.dating_profile.di.providers import providers as dating_profile_providers
from app.application.interaction.di.providers import providers as interaction_providers
from app.application.notification_device.di.providers import providers as notification_device_providers
from app.application.profile.di.providers import providers as profile_providers
from app.application.recommendation.di.providers import providers as recommendation_providers
from app.infra.config.di.providers import providers as config_providers
from app.infra.ml.di.providers import providers as ml_providers
from app.infra.notifications.di.providers import providers as notification_providers
from app.infra.oauth.di.providers import providers as oauth_providers
from app.infra.persistence.sqla.di.providers import providers as sqla_providers
from app.infra.security.di.providers import providers as security_providers
from tests.integration.di.identity_provider import TestIdentityProvider


class TestIdentityProviderProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    def identity_provider(self) -> IdentityProvider:
        return TestIdentityProvider()


def build_test_container() -> AsyncContainer:
    return make_async_container(
        *config_providers,
        *sqla_providers,
        *security_providers,
        *oauth_providers,
        *ml_providers,
        *auth_identity_providers,
        *notification_providers,
        TestIdentityProviderProvider(),
        *notification_device_providers,
        *profile_providers,
        *recommendation_providers,
        *dating_profile_providers,
        *interaction_providers,
        validation_settings=STRICT_VALIDATION,
    )
