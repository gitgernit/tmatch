import asyncio
from typing import override

from firebase_admin import messaging  # type: ignore[import-untyped]
from firebase_admin.messaging import Message, Notification  # type: ignore[import-untyped]

from app.application.common.notifications.service import NotificationService


class FCMNotificationService(NotificationService):
    @override
    async def send_notification(self, identifier: str, title: str, body: str) -> None:
        message = Message(
            token=identifier,
            notification=Notification(title=title, body=body),
        )
        await asyncio.to_thread(messaging.send, message)
