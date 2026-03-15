from app.application.common.identity_provider import IdentityProvider
from app.application.common.interactor import interactor
from app.application.targeting.data_gateway import TargetingDataGateway
from app.application.targeting.dto import TargetingResult
from app.application.targeting.errors import TargetingNotFoundError


@interactor
class GetMyTargetingInteractor:
    identity_provider: IdentityProvider
    targeting_data_gateway: TargetingDataGateway

    async def execute(self) -> TargetingResult:
        user = await self.identity_provider.get_current_user()
        targeting = await self.targeting_data_gateway.load_by_user_id(user.id)
        if targeting is None:
            raise TargetingNotFoundError
        return TargetingResult(rules=targeting.rules)
