from collections.abc import AsyncIterable
from urllib.parse import quote_plus

from dishka import BaseScope, Provider, Scope, WithParents, provide, provide_all
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from app.infra.persistence.sqla.bootstrapper import SqlaPersistenceBootstrapper
from app.infra.persistence.sqla.readiness import SqlaReadinessChecker
from app.infra.persistence.sqla.data_gateways.access_token import DefaultAccessTokenDataGateway
from app.infra.persistence.sqla.data_gateways.user import DefaultUserDataGateway
from app.infra.persistence.sqla.uow import DefaultUnitOfWork
from app.presentation.api.bootstrap.persistence_bootstrapper import PersistenceBootstrapper
from app.presentation.api.bootstrap.readiness_checker import ReadinessChecker
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

    persistence_bootstrapper = provide(
        source=SqlaPersistenceBootstrapper,
        provides=PersistenceBootstrapper,
        scope=Scope.APP,
    )
    readiness_checker = provide(
        source=SqlaReadinessChecker,
        provides=ReadinessChecker,
        scope=Scope.APP,
    )


class DataGatewayProvider(Provider):
    scope: BaseScope | None = Scope.REQUEST

    unit_of_work = provide(WithParents[DefaultUnitOfWork], scope=Scope.REQUEST)
    data_gateways = provide_all(
        WithParents[DefaultUserDataGateway],
        WithParents[DefaultAccessTokenDataGateway],
    )


providers = [
    SqlaProvider(),
    DataGatewayProvider(),
]
