from abc import abstractmethod
from typing import Protocol


class NotificationService(Protocol):
    @abstractmethod
    async def send_notification(self, identifier: str, title: str, body: str) -> None:
        raise NotImplementedError
