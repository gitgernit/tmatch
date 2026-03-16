from app.application.common.identity_provider import IdentityProvider
from app.application.common.interactor import interactor
from app.application.common.notifications.service import NotificationService
from app.application.common.unit_of_work import UnitOfWork
from app.application.interaction.dto import InteractionResult
from app.application.interaction.errors import (
    CandidateNotFoundError,
    CandidateNotRecommendedError,
    SelfInteractionError,
)
from app.application.match.data_gateway import MatchDataGateway
from app.application.notification_device.data_gateway import NotificationDeviceDataGateway
from app.application.recommendation.data_gateway import RecommendationDataGateway
from app.application.user.data_gateway import UserDataGateway
from app.domain.audit_event.entity import AuditEvent
from app.domain.audit_event.value_objects import AuditEventType
from app.domain.interaction.entity import Interaction
from app.domain.interaction.value_objects import InteractionType
from app.domain.user.entity import UserId


@interactor
class CreateInteractionInteractor:
    identity_provider: IdentityProvider
    unit_of_work: UnitOfWork
    user_data_gateway: UserDataGateway
    notification_device_data_gateway: NotificationDeviceDataGateway
    notification_service: NotificationService
    match_data_gateway: MatchDataGateway
    recommendation_data_gateway: RecommendationDataGateway

    async def execute(
        self,
        *,
        candidate_user_id: UserId,
        action: InteractionType,
        ml_recommendation_id: str | None = None,
    ) -> InteractionResult:
        user = await self.identity_provider.get_current_user()
        if user.id == candidate_user_id:
            raise SelfInteractionError
        candidate = await self.user_data_gateway.load_with_id(candidate_user_id)
        if candidate is None:
            raise CandidateNotFoundError
        if action in (InteractionType.LIKE, InteractionType.DISLIKE):
            is_recommended = await self.recommendation_data_gateway.has_recommendation(
                user_id=user.id,
                candidate_user_id=candidate_user_id,
                ml_recommendation_id=ml_recommendation_id,
            )
            if not is_recommended:
                raise CandidateNotRecommendedError
        interaction = Interaction.factory(
            actor_user_id=user.id,
            candidate_user_id=candidate_user_id,
            action=action,
            ml_recommendation_id=ml_recommendation_id,
        )
        payload = {"ml_recommendation_id": ml_recommendation_id} if ml_recommendation_id else {}
        audit_event = AuditEvent.factory(
            event_type=AuditEventType.INTERACTION_CREATED,
            actor_user_id=user.id,
            target_user_id=candidate_user_id,
            payload=payload,
        )
        await self.unit_of_work.add(interaction)
        await self.unit_of_work.add(audit_event)
        await self.unit_of_work.commit()
        if action is InteractionType.LIKE:
            await self._send_like_notifications(actor_id=user.id, candidate_user_id=candidate_user_id)
        return InteractionResult(
            interaction_id=interaction.id,
            actor_user_id=user.id,
            candidate_user_id=candidate_user_id,
            action=action,
            ml_recommendation_id=ml_recommendation_id,
            created_at=interaction.created_at,
        )

    async def _send_like_notifications(self, actor_id: UserId, candidate_user_id: UserId) -> None:
        candidate_device = await self.notification_device_data_gateway.load_by_user_id(candidate_user_id)
        if candidate_device is not None:
            await self.notification_service.send_notification(
                identifier=candidate_device.device_id,
                title="New like",
                body="You have a new like.",
            )

        match_user_ids = await self.match_data_gateway.list_active_match_user_ids(actor_id)
        is_match_active = candidate_user_id in match_user_ids
        if not is_match_active:
            return

        candidate_match_device = await self.notification_device_data_gateway.load_by_user_id(candidate_user_id)
        if candidate_match_device is not None:
            await self.notification_service.send_notification(
                identifier=candidate_match_device.device_id,
                title="New match",
                body="You have a new match.",
            )
