from uuid import UUID

from app.application.common.identity_provider import IdentityProvider
from app.application.common.interactor import interactor
from app.application.common.unit_of_work import UnitOfWork
from app.application.dating_profile.data_gateway import DatingProfileDataGateway
from app.application.profile.errors import ProfileNotFoundError
from app.application.recommendation.dto import RecommendationsResult
from app.application.recommendation.protocol import RecommendationProvider
from app.domain.recommendation.entity import Recommendation
from app.domain.recommendation.value_objects import RecommendationReason
from app.domain.user.entity import UserId


@interactor
class GetRecommendationsInteractor:
    identity_provider: IdentityProvider
    recommendation_provider: RecommendationProvider
    unit_of_work: UnitOfWork
    dating_profile_data_gateway: DatingProfileDataGateway

    async def execute(self, *, limit: int) -> RecommendationsResult:
        user = await self.identity_provider.get_current_user()
        dating_profile = await self.dating_profile_data_gateway.load_by_user_id(
            user.id,
        )
        if dating_profile is None or len(dating_profile.photos) < 1:
            raise ProfileNotFoundError
        items = await self.recommendation_provider.get_recommendations(user_id=user.id, limit=limit)
        for item in items:
            recommendation = Recommendation.factory(
                ml_recommendation_id=item.ml_recommendation_id,
                user_id=user.id,
                candidate_user_id=UserId(UUID(item.candidate_user_id)),
                reasons=[
                    RecommendationReason(
                        score=reason.score,
                        reason_type=reason.reason_type,
                    )
                    for reason in item.reasons
                ],
            )
            await self.unit_of_work.add(recommendation)
        await self.unit_of_work.commit()
        return RecommendationsResult(items=items)
