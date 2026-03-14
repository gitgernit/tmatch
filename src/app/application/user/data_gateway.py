from abc import abstractmethod
from typing import Protocol

from app.domain.user.entity import User, UserId


class UserDataGateway(Protocol):
    @abstractmethod
    async def load_with_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def list_user_ids(
        self,
        limit: int,
        exclude_user_id: UserId | None = None,
    ) -> list[UserId]:
        raise NotImplementedError
