from litestar import Litestar
import uvicorn

import asyncio

from app.adapters.api.routes.healthcheck.router import router as healthcheck_router

app = Litestar(route_handlers=[healthcheck_router])


async def main() -> None:
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
    )
    server = uvicorn.Server(config)

    try:
        await asyncio.gather(
            server.serve(),
        )

    except asyncio.CancelledError:
        await asyncio.gather(
            server.shutdown(),
        )


if __name__ == "__main__":
    asyncio.run(main())
