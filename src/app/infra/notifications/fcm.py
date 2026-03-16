import asyncio
from typing import override

from firebase_admin import messaging
from firebase_admin.messaging import Message, Notification
from structlog import get_logger

from app.application.common.notifications.service import NotificationService


logger = get_logger(__name__)


class FCMNotificationService(NotificationService):
    @override
    async def send_notification(self, identifier: str, title: str, body: str) -> None:
        message = Message(
            token=identifier,
            notification=Notification(title=title, body=body),
        )
        try:
            await asyncio.to_thread(messaging.send, message)
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "fcm_notification_send_failed",
                identifier=identifier,
                title=title,
                body=body,
                error=str(exc),
            )
