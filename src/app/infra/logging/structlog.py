import logging
from collections.abc import MutableMapping
from typing import Any

import structlog.processors
from opentelemetry.trace import get_current_span
from structlog.types import Processor


def add_trace_id_processor(
    _logger: object,
    _method_name: str,
    event_dict: MutableMapping[str, Any],
) -> MutableMapping[str, Any]:
    span = get_current_span()
    ctx = span.get_span_context()
    if ctx.is_valid:
        event_dict["trace_id"] = format(ctx.trace_id, "032x")
        event_dict["span_id"] = format(ctx.span_id, "016x")
    return event_dict


async def build_processors() -> list[Processor]:
    timestamp_processor = structlog.processors.TimeStamper(fmt="iso", utc=True, key="@timestamp")

    processors: list[Processor] = [
        structlog.processors.add_log_level,
        timestamp_processor,
        add_trace_id_processor,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    return processors


async def configure_logging() -> None:
    processors = await build_processors()
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(),
        foreign_pre_chain=processors,
    )

    logging.basicConfig(
        format="%(message)s",
        handlers=[logging.StreamHandler()],
        level=logging.INFO,
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    for foreign_logger in [
        "uvicorn",
        "uvicorn.access",
        "uvicorn.asgi",
        "uvicorn.error",
        "fastapi",
        "custom",
        "httpx",
        "httpcore",
    ]:
        logger = logging.getLogger(foreign_logger)
        logger.handlers = [handler]
        logger.propagate = False

    structlog.configure(
        processors=[*processors, structlog.processors.JSONRenderer()],
        context_class=dict,
        cache_logger_on_first_use=True,
    )
