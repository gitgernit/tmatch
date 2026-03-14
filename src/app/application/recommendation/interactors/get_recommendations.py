from uuid import UUID

from app.application.common.identity_provider import IdentityProvider
from app.application.common.interactor import interactor
from app.application.common.unit_of_work import UnitOfWork
from app.application.profile.errors import ProfileNotFoundError
from app.application.recommendation.dto import RecommendationsResult
from app.application.recommendation.protocol import RecommendationProvider
from app.domain.audit_event.entity import AuditEvent
from app.domain.audit_event.value_objects import AuditEventType
from app.domain.recommendation.entity import Recommendation
from app.domain.user.entity import UserId


@interactor
class GetRecommendationsInteractor:
    identity_provider: IdentityProvider
    recommendation_provider: RecommendationProvider
    unit_of_work: UnitOfWork

    async def execute(self, *, limit: int) -> RecommendationsResult:
        user = await self.identity_provider.get_current_user()
        if user.profile is None:
            raise ProfileNotFoundError
        items = await self.recommendation_provider.get_recommendations(user_id=user.id, limit=limit)
        for item in items:
            recommendation = Recommendation.factory(
                user_id=user.id,
                candidate_user_id=UserId(UUID(item.candidate_user_id)),
                score=item.score,
                reason_type=item.reason_type,
                reason_details=item.reason_details,
            )
            await self.unit_of_work.add(recommendation)
        audit_event = AuditEvent.factory(
            event_type=AuditEventType.RECOMMENDATION_SHOWN,
            actor_user_id=user.id,
            payload={"candidate_user_ids": [item.candidate_user_id for item in items]},
        )
        await self.unit_of_work.add(audit_event)
        await self.unit_of_work.commit()
        return RecommendationsResult(items=items)

