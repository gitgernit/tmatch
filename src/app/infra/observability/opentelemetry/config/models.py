from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OpentelemetryConfig:
    """Конфигурация OpenTelemetry.

    Attributes:
        metrics_exporter: Экспортер метрик
        logs_exporter: Экспортер логов
        traces_exporter: Экспортер трейсов
        exporter_otlp_traces_certificate: Сертификат для экспортера OTLP трейсов
        exporter_otlp_endpoint: GRPC эндпоинт для экспортера OTLP
        is_tracing_enabled: Включен ли трейсинг

    """

    metrics_exporter: str
    logs_exporter: str
    traces_exporter: str
    exporter_otlp_traces_certificate: str
    exporter_otlp_endpoint: str
    is_tracing_enabled: bool
