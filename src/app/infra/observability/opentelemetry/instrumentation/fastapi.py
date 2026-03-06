from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from adviser.infra.observability.opentelemetry.config.models import OpentelemetryConfig


class FastapiOpentelemetryInstrumentor:
    def __init__(self, config: OpentelemetryConfig) -> None:
        self.config = config

    def instrument(self, app: FastAPI, excluded_urls: list[str] | None = None) -> None:
        excluded_urls = excluded_urls or []

        FastAPIInstrumentor().instrument_app(
            app=app,
            excluded_urls=",".join(excluded_urls),
        )
