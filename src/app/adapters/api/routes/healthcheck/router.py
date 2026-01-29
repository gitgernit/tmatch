from litestar import get, Router
from litestar.status_codes import HTTP_200_OK

from typing import Literal


@get(
    path="/liveness",
    status_code=HTTP_200_OK,
    summary="Service liveness probe",
)
async def liveness_probe() -> dict[Literal["status"], Literal["ok"]]:
    return {
        "status": "ok",
    }


router = Router(
    path="/",
    route_handlers=[liveness_probe],
)
