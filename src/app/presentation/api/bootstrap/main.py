import asyncio
import sys

import firebase_admin  # type: ignore[import-untyped]
import uvicorn
from dishka import AsyncContainer
from dishka.integrations.litestar import setup_dishka
from dotenv import load_dotenv
from firebase_admin import credentials  # type: ignore[import-untyped]
from litestar import Litestar
from litestar.contrib.opentelemetry import OpenTelemetryConfig, OpenTelemetryPlugin

from app.infra.logging.structlog import configure_logging
from app.infra.observability.opentelemetry.instrumentation.tracing import setup_tracing
from app.presentation.api.bootstrap.di.container import build_container
from app.presentation.api.bootstrap.persistence_bootstrapper import PersistenceBootstrapper
from app.presentation.api.config.models import FirebaseConfig, OpentelemetryConfig, ServerConfig
from app.presentation.api.routes.auth.router import router as auth_router
from app.presentation.api.routes.healthcheck.router import router as healthcheck_router
from app.presentation.api.routes.metrics.middleware import metrics_middleware
from app.presentation.api.routes.metrics.router import router as metrics_router
from app.presentation.api.routes.notifications.router import router as notifications_router


def create_app(
    container: AsyncContainer,
    otel_config: OpentelemetryConfig,
) -> Litestar:
    tracer_provider = setup_tracing(otel_config)
    litestar_otel_config = OpenTelemetryConfig(tracer_provider=tracer_provider)

    app = Litestar(
        route_handlers=[healthcheck_router, auth_router, metrics_router, notifications_router],
        middleware=[metrics_middleware],
        plugins=[OpenTelemetryPlugin(config=litestar_otel_config)],
    )
    setup_dishka(container=container, app=app)
    return app


async def main() -> None:
    await configure_logging()

    container = build_container()
    try:
        persistence_bootstrapper = await container.get(PersistenceBootstrapper)
        await persistence_bootstrapper.bootstrap()

        firebase_config = await container.get(FirebaseConfig)
        if firebase_config.certificate_path:
            cred = credentials.Certificate(firebase_config.certificate_path)
            firebase_admin.initialize_app(cred)

        server_config = await container.get(ServerConfig)
        otel_config = await container.get(OpentelemetryConfig)
        app = create_app(container, otel_config)
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
