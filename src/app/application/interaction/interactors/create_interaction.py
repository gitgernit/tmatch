from app.application.common.identity_provider import IdentityProvider
from app.application.common.interactor import interactor
from app.application.common.unit_of_work import UnitOfWork
from app.application.interaction.dto import InteractionResult
from app.application.interaction.errors import CandidateNotFoundError, SelfInteractionError
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
        return InteractionResult(
            interaction_id=interaction.id,
            actor_user_id=user.id,
            candidate_user_id=candidate_user_id,
            action=action,
            ml_recommendation_id=ml_recommendation_id,
            created_at=interaction.created_at,
        )
