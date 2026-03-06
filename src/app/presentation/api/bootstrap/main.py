import asyncio
import sys

import uvicorn
from dishka import AsyncContainer
from dishka.integrations.litestar import setup_dishka
from dotenv import load_dotenv
from litestar import Litestar

from app.infra.logging.structlog import configure_logging
from app.presentation.api.bootstrap.di.container import build_container
from app.presentation.api.bootstrap.persistence_bootstrapper import PersistenceBootstrapper
from app.presentation.api.config.models import ServerConfig
from app.presentation.api.routes.auth.router import router as auth_router
from app.presentation.api.routes.healthcheck.router import router as healthcheck_router


def create_app(container: AsyncContainer) -> Litestar:
    app = Litestar(route_handlers=[healthcheck_router, auth_router])
    setup_dishka(container=container, app=app)
    return app


async def main() -> None:
    await configure_logging()

    container = build_container()
    try:
        persistence_bootstrapper = await container.get(PersistenceBootstrapper)
        await persistence_bootstrapper.bootstrap()

        server_config = await container.get(ServerConfig)
        app = create_app(container)
        config = uvicorn.Config(
            app,
            workers=server_config.workers,
            host=server_config.host,
            port=server_config.port,
            log_level="info",
            log_config=None,
        )
        server = uvicorn.Server(config)

        async with asyncio.TaskGroup() as tg:
            _ = tg.create_task(server.serve())
    finally:
        await container.close()


def sync_entrypoint() -> None:
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    load_dotenv(override=False)

    asyncio.run(main())


if __name__ == "__main__":
    sync_entrypoint()
