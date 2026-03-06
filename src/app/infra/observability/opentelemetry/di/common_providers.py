from dishka import BaseScope, Provider, Scope, provide_all

from adviser.infra.observability.opentelemetry.instrumentation.common import CommonOpentelemetryInstrumentor


class InstrumentorProvider(Provider):
    scope: BaseScope | None = Scope.APP

    instrumentors = provide_all(
        CommonOpentelemetryInstrumentor,
    )


providers = [
    InstrumentorProvider(),
]
