from dataclasses import asdict
from typing import Any, override

from dishka.integrations.litestar import FromDishka
from litestar import WebSocket, websocket
from litestar.status_codes import WS_1008_POLICY_VIOLATION

from app.application.chat.dto import ChatMessageItem
from app.application.common.identity_provider import IdentityProvider
from app.application.common.messaging.service import MessageConsumer, MessagingService


class WebSocketChatConsumer(MessageConsumer):
    def __init__(self, websocket: WebSocket[Any, Any, Any], user_id: str) -> None:
        self._websocket = websocket
        self._user_id = user_id

    @override
    async def deliver(self, message: ChatMessageItem) -> None:
        payload = {
            "type": "message",
            **asdict(message),
        }
        await self._websocket.send_json(payload)


@websocket(path="/chat/stream")
async def chat_websocket_handler(
    socket: WebSocket[Any, Any, Any],
    identity_provider: FromDishka[IdentityProvider],
    messaging_service: FromDishka[MessagingService],
) -> None:
    token = socket.query_params.get("token")
    if not token:
        await socket.close(code=WS_1008_POLICY_VIOLATION)
        return

    # Переиспользуем существующий IdentityProvider: он уже знает, как работать с токенами.
    user = await identity_provider.get_current_user()

    await socket.accept()
    consumer = WebSocketChatConsumer(socket, str(user.id))
    messaging_service.register(user.id, consumer)

    try:
        # На MVP сервер только пушит сообщения, клиент может посылать ping/pong по своему усмотрению.
        while True:
            _ = await socket.receive_json()
    finally:
        messaging_service.unregister(user.id, consumer)
