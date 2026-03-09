from typing import override

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.notification_device.data_gateway import NotificationDeviceDataGateway
from app.domain.notification_device.entity import NotificationDevice
from app.domain.user.entity import UserId
from app.infra.persistence.sqla.tables import notification_device_table


class DefaultNotificationDeviceDataGateway(NotificationDeviceDataGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def load_by_user_id(self, user_id: UserId) -> NotificationDevice | None:
        statement = select(NotificationDevice).where(notification_device_table.c.user_id == user_id)
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    @override
    async def load_by_user_id_and_device_id(
        self,
        user_id: UserId,
        device_id: str,
    ) -> NotificationDevice | None:
        statement = select(NotificationDevice).where(
            notification_device_table.c.user_id == user_id,
            notification_device_table.c.device_id == device_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
