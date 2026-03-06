from dishka import BaseScope, Provider, Scope, provide_all

from adviser.infra.observability.opentelemetry.instrumentation.fastapi import FastapiOpentelemetryInstrumentor


class InstrumentorProvider(Provider):
    scope: BaseScope | None = Scope.APP

    instrumentors = provide_all(
        FastapiOpentelemetryInstrumentor,
    )


providers = [
    InstrumentorProvider(),
]
