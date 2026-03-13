from app.application.common.dto import dto
from app.domain.user.value_objects import Profile


@dto
class ProfileResult:
    user_id: str
    profile: Profile
