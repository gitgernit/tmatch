from cryptography.fernet import Fernet
from dishka import BaseScope, Provider, Scope, WithParents, provide, provide_all

from app.infra.security.access_token.cryptographer import FernetAccessTokenCryptographer
from app.infra.security.access_token.factory import DefaultAccessTokenFactory
from app.presentation.api.config.models import AccessTokenConfig


class AccessTokenProvider(Provider):
    scope: BaseScope | None = Scope.APP

    @provide
    def fernet(self, configuration: AccessTokenConfig) -> Fernet:
        return Fernet(configuration.crypto_key)

    provides = provide_all(
        WithParents[FernetAccessTokenCryptographer],
        WithParents[DefaultAccessTokenFactory],
    )


providers = [
    AccessTokenProvider(),
]
