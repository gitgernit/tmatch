from app.application.chat.data_gateway import ChatDataGateway
from app.application.chat.dto import ChatItemResult, ChatListResult
from app.application.common.identity_provider import IdentityProvider
from app.application.common.interactor import interactor
from app.domain.user.entity import UserId


def _get_other_user_id(current_user_id: UserId, user_a_id: UserId, user_b_id: UserId) -> UserId:
    if current_user_id == user_a_id:
        return user_b_id
    return user_a_id


@interactor
class GetMyChatsInteractor:
    identity_provider: IdentityProvider
    chat_data_gateway: ChatDataGateway

    async def execute(self) -> ChatListResult:
        user = await self.identity_provider.get_current_user()
        chats = await self.chat_data_gateway.list_chats_for_user(user.id)

        items: list[ChatItemResult] = []
        for chat in chats:
            other_user_id = _get_other_user_id(user.id, chat.user_a_id, chat.user_b_id)
            last_messages = await self.chat_data_gateway.list_messages(
                chat_id=chat.id,
                limit=1,
                before_message_id=None,
            )
            last = last_messages[0] if last_messages else None
            items.append(
                ChatItemResult(
                    chat_id=chat.id,
                    other_user_id=other_user_id,
                    last_message_id=last.id if last else None,
                    last_message_text=last.text if last else None,
                    last_message_created_at=last.created_at if last else None,
                ),
            )
        return ChatListResult(items=items)
