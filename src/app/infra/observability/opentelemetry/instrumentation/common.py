from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from adviser.infra.observability.opentelemetry.config.models import OpentelemetryConfig


class CommonOpentelemetryInstrumentor:
    def __init__(self, config: OpentelemetryConfig) -> None:
        self.config = config

    def setup_tracing_provider(self) -> None:
        tracer_provider = TracerProvider()
        trace.set_tracer_provider(tracer_provider)

        exporter: OTLPSpanExporter | ConsoleSpanExporter

        if self.config.traces_exporter == "otlp":
            exporter = OTLPSpanExporter(
                endpoint=self.config.exporter_otlp_endpoint,
                insecure=False,
            )

        elif self.config.traces_exporter == "console":
            exporter = ConsoleSpanExporter()

        else:
            msg = f"Unknown traces exporter: {self.config.traces_exporter}"
            raise ValueError(msg)

        tracer_provider.add_span_processor(BatchSpanProcessor(exporter))

    def instrument(self) -> None:
        RequestsInstrumentor().instrument()
