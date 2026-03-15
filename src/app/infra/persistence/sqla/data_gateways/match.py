from typing import override

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.match.data_gateway import MatchDataGateway
from app.domain.interaction.value_objects import InteractionType
from app.domain.user.entity import UserId

# Latest interaction per (actor, candidate); then mutual like => match.
_MATCH_IDS_QUERY = text("""
WITH latest AS (
    SELECT DISTINCT ON (actor_user_id, candidate_user_id)
        actor_user_id, candidate_user_id, action
    FROM interactions
    WHERE deleted_at IS NULL
    ORDER BY actor_user_id, candidate_user_id, created_at DESC
)
SELECT l1.candidate_user_id AS user_id
FROM latest l1
JOIN latest l2
    ON l2.actor_user_id = l1.candidate_user_id
    AND l2.candidate_user_id = l1.actor_user_id
WHERE l1.actor_user_id = :user_id
  AND l1.action = :like_action
  AND l2.action = :like_action
""")


class DefaultMatchDataGateway(MatchDataGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @override
    async def list_active_match_user_ids(self, user_id: UserId) -> list[UserId]:
        result = await self._session.execute(
            _MATCH_IDS_QUERY,
            {"user_id": user_id, "like_action": InteractionType.LIKE.value},
        )
        rows = result.fetchall()
        return [UserId(row[0]) for row in rows if row[0] is not None]
