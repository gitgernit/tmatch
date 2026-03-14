from dishka.integrations.litestar import DishkaRouter, FromDishka
from litestar import get, patch, put
from litestar.exceptions import HTTPException
from litestar.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from app.application.auth_identity.errors import UserUnauthorizedError
from app.application.dating_profile.errors import (
    DatingProfileNotFoundError,
    DatingProfileValidationError,
    ProfileRequiredError,
)
from app.application.dating_profile.interactors.get_dating_profile import (
    GetDatingProfileInteractor,
)
from app.application.dating_profile.interactors.set_trait_visibility import (
    SetTraitVisibilityInteractor,
)
from app.application.dating_profile.interactors.upsert_dating_profile import (
    UpsertDatingProfileInteractor,
)
from app.presentation.api.routes.dating_profile.dto import (
    DatingProfileResponse,
    SetTraitVisibilityRequest,
    TraitItemResponse,
    UpsertDatingProfileRequest,
)


@get(
    path="/me",
    summary="Get own dating profile",
    security=[{"BearerToken": []}],
)
async def get_dating_profile(
    interactor: FromDishka[GetDatingProfileInteractor],
) -> DatingProfileResponse:
    try:
        result = await interactor.execute()
    except UserUnauthorizedError as error:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        ) from error
    except DatingProfileNotFoundError as error:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Dating profile not found",
        ) from error
    p = result.dating_profile
    return DatingProfileResponse(
        user_id=p.user_id,
        photos=p.photos,
        traits=[
            TraitItemResponse(
                trait_code=t.trait_code,
                score=t.score,
                is_hidden=t.is_hidden,
            )
            for t in p.traits
        ],
    )


@put(
    path="/me",
    summary="Create or update own dating profile",
    security=[{"BearerToken": []}],
)
async def upsert_dating_profile(
    data: UpsertDatingProfileRequest,
    interactor: FromDishka[UpsertDatingProfileInteractor],
) -> DatingProfileResponse:
    try:
        result = await interactor.execute(photos=data.photos)
    except UserUnauthorizedError as error:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        ) from error
    except ProfileRequiredError as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Profile required to create dating profile",
        ) from error
    except DatingProfileValidationError as error:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="At least one photo required",
        ) from error
    p = result.dating_profile
    return DatingProfileResponse(
        user_id=p.user_id,
        photos=p.photos,
        traits=[
            TraitItemResponse(
                trait_code=t.trait_code,
                score=t.score,
                is_hidden=t.is_hidden,
            )
            for t in p.traits
        ],
    )


@patch(
    path="/me/traits/visibility",
    summary="Set trait visibility (hide/show)",
    security=[{"BearerToken": []}],
    status_code=204,
)
async def set_trait_visibility(
    data: SetTraitVisibilityRequest,
    interactor: FromDishka[SetTraitVisibilityInteractor],
) -> None:
    try:
        await interactor.execute(
            trait_code=data.trait_code,
            is_hidden=data.is_hidden,
        )
    except UserUnauthorizedError as error:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        ) from error
    except DatingProfileNotFoundError as error:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Dating profile or trait not found",
        ) from error


router = DishkaRouter(
    path="/dating-profile",
    route_handlers=[get_dating_profile, upsert_dating_profile, set_trait_visibility],
    tags=["dating-profile"],
)
