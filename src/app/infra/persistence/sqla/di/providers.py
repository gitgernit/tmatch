from collections.abc import AsyncIterable
from urllib.parse import quote_plus

from dishka import BaseScope, Provider, Scope, WithParents, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from app.infra.persistence.sqla.uow import DefaultUnitOfWork
from app.presentation.api.config.models import PostgresConfig


def _build_url(config: PostgresConfig) -> str:
    password = quote_plus(config.password)
    return f"postgresql+psycopg://{config.user}:{password}@{config.host}:{config.port}/{config.db}"


class SqlaProvider(Provider):
    scope: BaseScope | None = Scope.APP

    @provide(scope=Scope.APP)
    async def engine(self, postgres_config: PostgresConfig) -> AsyncIterable[AsyncEngine]:
        url = _build_url(postgres_config)
        engine = create_async_engine(url)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.REQUEST)
    async def async_session(self, engine: AsyncEngine) -> AsyncIterable[AsyncSession]:
        session = AsyncSession(bind=engine, expire_on_commit=False)
        async with session:
            yield session

    unit_of_work = provide(WithParents[DefaultUnitOfWork], scope=Scope.REQUEST)


providers = [
    SqlaProvider(),
]
