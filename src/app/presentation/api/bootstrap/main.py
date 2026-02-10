import asyncio

import uvicorn
from litestar import Litestar

from app.presentation.api.bootstrap.di.container import build_container
from app.presentation.api.config.models import ServerConfig
from app.presentation.api.routes.healthcheck.router import router as healthcheck_router


def create_app() -> Litestar:
    return Litestar(route_handlers=[healthcheck_router])


async def main() -> None:
    container = build_container()

    server_config = await container.get(ServerConfig)

    app = create_app()
    config = uvicorn.Config(
        app,
        workers=server_config.workers,
        host=server_config.host,
        port=server_config.port,
        log_level="info",
    )
    server = uvicorn.Server(config)

    async with asyncio.TaskGroup() as tg:
        _ = tg.create_task(server.serve())


def sync_entrypoint() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    sync_entrypoint()
