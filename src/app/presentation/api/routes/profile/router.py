from dishka.integrations.litestar import DishkaRouter, FromDishka
from litestar import get, put
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

from app.application.auth_identity.errors import UserUnauthorizedError
from app.application.profile.errors import ProfileNotFoundError
from app.application.profile.interactors.get_profile import GetProfileInteractor
from app.application.profile.interactors.upsert_profile import UpsertProfileInteractor
from app.presentation.api.routes.profile.dto import ProfileResponse, UpsertProfileRequest


@get(
    path="/",
    summary="Get own profile",
    security=[{"BearerToken": []}],
)
async def get_profile(
    interactor: FromDishka[GetProfileInteractor],
) -> ProfileResponse:
    try:
        result = await interactor.execute()
    except UserUnauthorizedError as error:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized") from error
    except ProfileNotFoundError as error:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Profile not set yet") from error

    p = result.profile
    return ProfileResponse(
        user_id=result.user_id,
        first_name=p.first_name,
        last_name=p.last_name,
        birth_date=p.birth_date,
        region=p.region,
        avatar_url=p.avatar_url,
    )


@put(
    path="/",
    summary="Create or update own profile",
    security=[{"BearerToken": []}],
)
async def upsert_profile(
    data: UpsertProfileRequest,
    interactor: FromDishka[UpsertProfileInteractor],
) -> ProfileResponse:
    try:
        result = await interactor.execute(
            first_name=data.first_name,
            last_name=data.last_name,
            birth_date=data.birth_date,
            region=data.region,
            avatar_url=data.avatar_url,
        )
    except UserUnauthorizedError as error:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized") from error

    p = result.profile
    return ProfileResponse(
        user_id=result.user_id,
        first_name=p.first_name,
        last_name=p.last_name,
        birth_date=p.birth_date,
        region=p.region,
        avatar_url=p.avatar_url,
    )


router = DishkaRouter(
    path="/profile",
    route_handlers=[get_profile, upsert_profile],
    tags=["profile"],
)
