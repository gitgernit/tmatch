from dishka import BaseScope, Provider, Scope, provide

from app.application.recommendation.protocol import RecommendationProvider
from app.application.user.data_gateway import UserDataGateway
from app.infra.ml.mock_recommendation_provider import MockRecommendationProvider
from app.presentation.api.config.models import MlConfig


class RecommendationProviderInfraProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    def recommendation_provider(
        self,
        config: MlConfig,
        user_gateway: UserDataGateway,
    ) -> RecommendationProvider:
        if config.recommendation_provider == "mock":
            return MockRecommendationProvider(user_gateway=user_gateway)
        msg = f"Unknown ML recommendation provider: {config.recommendation_provider!r}"
        raise ValueError(msg)


providers = [
    RecommendationProviderInfraProvider(),
]
