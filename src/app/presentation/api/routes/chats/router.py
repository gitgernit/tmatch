from uuid import UUID

from dishka.integrations.litestar import DishkaRouter, FromDishka
from litestar import get, post
from litestar.exceptions import HTTPException
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from app.application.auth_identity.errors import UserUnauthorizedError
from app.application.chat.errors import (
    ChatAccessDeniedError,
    ChatBlockedError,
    ChatNoActiveMatchError,
    ChatNotFoundError,
    ChatValidationError,
)
from app.application.chat.interactors.get_chat_messages import GetChatMessagesInteractor
from app.application.chat.interactors.get_my_chats import GetMyChatsInteractor
from app.application.chat.interactors.send_chat_message import SendChatMessageInteractor
from app.domain.chat.entity import ChatId, MessageId
from app.presentation.api.routes.chats.dto import (
    ChatItemResponse,
    ChatMessageItemResponse,
    ChatMessagesResponse,
    ChatsResponse,
    SendMessageRequest,
)


@get(
    path="/me",
    summary="Get own chats",
    security=[{"BearerToken": []}],
)
async def get_my_chats(
    interactor: FromDishka[GetMyChatsInteractor],
) -> ChatsResponse:
    try:
        result = await interactor.execute()
    except UserUnauthorizedError as error:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized") from error

    items = [
        ChatItemResponse(
            chat_id=chat.chat_id,
            other_user_id=chat.other_user_id,
            last_message_id=chat.last_message_id,
            last_message_text=chat.last_message_text,
            last_message_created_at=chat.last_message_created_at,
        )
        for chat in result.items
    ]
    return ChatsResponse(items=items)


@get(
    path="/{chat_id:uuid}/messages",
    summary="Get chat messages",
    security=[{"BearerToken": []}],
)
async def get_chat_messages(
    chat_id: UUID,
    limit: int | None,
    before_message_id: UUID | None,
    interactor: FromDishka[GetChatMessagesInteractor],
) -> ChatMessagesResponse:
    try:
        result = await interactor.execute(
            chat_id=ChatId(chat_id),
            limit=limit or 50,
            before_message_id=MessageId(before_message_id) if before_message_id else None,
        )
    except UserUnauthorizedError as error:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized") from error
    except ChatNotFoundError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Chat not found") from error
    except ChatAccessDeniedError as error:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Chat access denied") from error

    items = [
        ChatMessageItemResponse(
            message_id=m.message_id,
            chat_id=m.chat_id,
            sender_user_id=m.sender_user_id,
            text=m.text,
            created_at=m.created_at,
        )
        for m in result.items
    ]
    return ChatMessagesResponse(items=items)


@post(
    path="/{chat_id:uuid}/messages",
    summary="Send text message to chat",
    security=[{"BearerToken": []}],
)
async def send_chat_message(
    chat_id: UUID,
    data: SendMessageRequest,
    interactor: FromDishka[SendChatMessageInteractor],
) -> ChatMessageItemResponse:
    try:
        result = await interactor.execute(
            chat_id=ChatId(chat_id),
            text=data.text,
        )
    except UserUnauthorizedError as error:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized") from error
    except ChatNotFoundError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Chat not found") from error
    except ChatAccessDeniedError as error:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Chat access denied") from error
    except ChatBlockedError as error:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Chat is blocked") from error
    except ChatNoActiveMatchError as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="No active match between participants",
        ) from error
    except ChatValidationError as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid message",
        ) from error

    return ChatMessageItemResponse(
        message_id=result.message_id,
        chat_id=result.chat_id,
        sender_user_id=result.sender_user_id,
        text=result.text,
        created_at=result.created_at,
    )


router = DishkaRouter(
    path="/chats",
    route_handlers=[get_my_chats, get_chat_messages, send_chat_message],
    tags=["chats"],
)
