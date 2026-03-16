from app.application.chat.data_gateway import ChatDataGateway
from app.application.chat.dto import ChatMessageItem
from app.application.chat.errors import (
    ChatAccessDeniedError,
    ChatBlockedError,
    ChatNoActiveMatchError,
    ChatNotFoundError,
    ChatValidationError,
)
from app.application.common.identity_provider import IdentityProvider
from app.application.common.interactor import interactor
from app.application.common.notifications.service import NotificationService
from app.application.common.unit_of_work import UnitOfWork
from app.application.interaction.blocked_pairs_gateway import BlockedPairsGateway
from app.application.match.data_gateway import MatchDataGateway
from app.application.notification_device.data_gateway import NotificationDeviceDataGateway
from app.domain.chat.entity import ChatId, Message
from app.domain.user.entity import UserId


def _get_other_user_id(current_user_id: UserId, user_a_id: UserId, user_b_id: UserId) -> UserId:
    if current_user_id == user_a_id:
        return user_b_id
    return user_a_id


@interactor
class SendChatMessageInteractor:
    identity_provider: IdentityProvider
    unit_of_work: UnitOfWork
    chat_data_gateway: ChatDataGateway
    match_data_gateway: MatchDataGateway
    blocked_pairs_gateway: BlockedPairsGateway
    notification_device_data_gateway: NotificationDeviceDataGateway
    notification_service: NotificationService

    async def execute(
        self,
        *,
        chat_id: ChatId,
        text: str,
    ) -> ChatMessageItem:
        text = text.strip()
        if not text:
            raise ChatValidationError

        user = await self.identity_provider.get_current_user()
        chat = await self.chat_data_gateway.load_chat_by_id(chat_id)
        if chat is None:
            raise ChatNotFoundError
        if user.id not in (chat.user_a_id, chat.user_b_id):
            raise ChatAccessDeniedError

        other_user_id = _get_other_user_id(user.id, chat.user_a_id, chat.user_b_id)

        blocked_user_ids = await self.blocked_pairs_gateway.list_blocked_user_ids(user.id)
        if other_user_id in blocked_user_ids:
            raise ChatBlockedError

        match_user_ids = await self.match_data_gateway.list_active_match_user_ids(user.id)
        if other_user_id not in match_user_ids:
            raise ChatNoActiveMatchError

        message = Message.factory(chat_id=chat.id, sender_user_id=user.id, text=text)
        await self.unit_of_work.add(message)
        await self.unit_of_work.commit()

        device = await self.notification_device_data_gateway.load_by_user_id(other_user_id)
        if device is not None:
            sender_name_parts: list[str] = []
            if user.profile is not None:
                sender_name_parts.append(user.profile.first_name)
                if user.profile.last_name:
                    sender_name_parts.append(user.profile.last_name)
            sender_name = " ".join(sender_name_parts) if sender_name_parts else "New message"
            await self.notification_service.send_notification(
                identifier=device.device_id,
                title=f"Message from {sender_name}",
                body=text,
            )

        return ChatMessageItem(
            message_id=message.id,
            chat_id=message.chat_id,
            sender_user_id=message.sender_user_id,
            text=message.text,
            created_at=message.created_at,
        )
