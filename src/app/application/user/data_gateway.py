from abc import abstractmethod
from typing import Protocol

from app.domain.user.entity import User, UserId


class UserDataGateway(Protocol):
    @abstractmethod
    async def load_with_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError
