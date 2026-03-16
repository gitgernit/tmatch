import os
import uuid
from collections.abc import AsyncGenerator
from os import getenv
from typing import cast

import pytest
from dishka import AsyncContainer
from dotenv import load_dotenv
from litestar import Litestar
from litestar.testing import TestClient

from app.application.common.identity_provider import IdentityProvider
from app.presentation.api.bootstrap.main import create_app
from app.presentation.api.bootstrap.persistence_bootstrapper import PersistenceBootstrapper
from app.presentation.api.config.models import OpentelemetryConfig
from tests.integration.di.container import build_http_ml_test_container, build_test_container

load_dotenv(override=False)
load_dotenv(".env.local", override=False)


@pytest.fixture(scope="session")
async def app() -> AsyncGenerator[Litestar, None]:
    os.environ.setdefault("OTEL_TRACES_EXPORTER", "none")
    container = build_test_container()
    async with container() as scope:
        bootstrapper = await scope.get(PersistenceBootstrapper)
        await bootstrapper.bootstrap()
        otel_config = await scope.get(OpentelemetryConfig)
        yield create_app(container, otel_config)


@pytest.fixture
def client(app: Litestar) -> TestClient[Litestar]:
    return TestClient(app=app)


@pytest.fixture
def test_run_suffix() -> str:
    return uuid.uuid4().hex[:12]


@pytest.fixture
async def ml_http_container() -> AsyncGenerator[AsyncContainer, None]:
    base_url = getenv("ML_TEST_BASE_URL") or getenv("ML_BASE_URL") or "http://127.0.0.1:8080"
    container = build_http_ml_test_container(
        base_url=base_url,
    )
    async with container() as request_scope:
        yield request_scope


@pytest.fixture
async def ml_http_identity_provider(ml_http_container: AsyncContainer) -> IdentityProvider:
    return cast("IdentityProvider", await ml_http_container.get(IdentityProvider))
