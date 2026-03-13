from datetime import date

from app.application.common.identity_provider import IdentityProvider
from app.application.common.interactor import interactor
from app.application.common.unit_of_work import UnitOfWork
from app.application.profile.dto import ProfileResult
from app.domain.user.value_objects import Profile


@interactor
class UpsertProfileInteractor:
    identity_provider: IdentityProvider
    unit_of_work: UnitOfWork

    async def execute(
        self,
        first_name: str,
        last_name: str | None,
        birth_date: date,
        region: str | None,
        avatar_url: str | None,
    ) -> ProfileResult:
        user = await self.identity_provider.get_current_user()
        profile = Profile(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            region=region,
            avatar_url=avatar_url,
        )
        user.profile = profile
        await self.unit_of_work.add(user)
        await self.unit_of_work.commit()
        return ProfileResult(user_id=str(user.id), profile=profile)
