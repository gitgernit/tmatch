from dishka.integrations.litestar import DishkaRouter, FromDishka
from litestar import get
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_503_SERVICE_UNAVAILABLE

from app.application.auth_identity.errors import UserUnauthorizedError
from app.application.profile.errors import ProfileNotFoundError
from app.application.recommendation.errors import RecommendationProviderUnavailableError
from app.application.recommendation.interactors.get_recommendations import GetRecommendationsInteractor
from app.presentation.api.routes.recommendations.dto import RecommendationsQuery, RecommendationsResponse


@get(
    path="/",
    summary="Get personalized candidates for current user",
    security=[{"BearerToken": []}],
)
async def get_recommendations(
    query: RecommendationsQuery,
    interactor: FromDishka[GetRecommendationsInteractor],
) -> RecommendationsResponse:
    try:
        result = await interactor.execute(limit=query.limit)
    except UserUnauthorizedError as error:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized") from error
    except ProfileNotFoundError as error:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Profile not set yet") from error
    except RecommendationProviderUnavailableError as error:
        raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error

    return RecommendationsResponse(
        items=[
            {
                "candidate_user_id": item.candidate_user_id,
                "score": item.score,
                "reason_type": item.reason_type,
                "reason_details": item.reason_details,
            }
            for item in result.items
        ],
    )


router = DishkaRouter(
    path="/recommendations",
    route_handlers=[get_recommendations],
    tags=["recommendations"],
)

