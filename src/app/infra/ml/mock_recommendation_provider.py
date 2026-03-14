from typing import override

from app.application.recommendation.dto import RecommendationItem
from app.application.recommendation.errors import RecommendationProviderUnavailableError
from app.application.recommendation.protocol import RecommendationProvider
from app.application.user.data_gateway import UserDataGateway
from app.domain.recommendation.value_objects import CompatibilityType
from app.domain.user.entity import UserId


class MockRecommendationProvider(RecommendationProvider):
    def __init__(self, user_gateway: UserDataGateway) -> None:
        self._user_gateway = user_gateway

    @override
    async def get_recommendations(self, *, user_id: UserId, limit: int) -> list[RecommendationItem]:
        try:
            candidate_ids = await self._user_gateway.list_user_ids(
                limit=limit,
                exclude_user_id=user_id,
            )
        except Exception as error:
            raise RecommendationProviderUnavailableError from error
        return [
            RecommendationItem(
                ml_recommendation_id=f"mock-{user_id}-{i + 1}",
                candidate_user_id=str(cid),
                score=1.0 - (i * 0.01),
                reason_type=CompatibilityType.LIFESTYLE,
                reason_details=None,
            )
            for i, cid in enumerate(candidate_ids)
        ]
