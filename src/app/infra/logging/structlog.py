import logging
import typing

import structlog.processors
from dishka import AsyncContainer
from structlog.types import EventDict, Processor

from adviser.infra.observability.sage.config.models import SageConfig


class SageProcessor:
    def __init__(self, sage_config: SageConfig) -> None:
        self._config = sage_config

    def __call__(self, logger: logging.Logger, method: str, event_dict: EventDict) -> EventDict:
        event_dict["env"] = self._config.env
        event_dict["system"] = self._config.system
        event_dict["component"] = self._config.component

        return event_dict


class LevelProcessor:
    LEVEL_MAP: typing.ClassVar[dict[str, str]] = {
        "debug": "DEBUG",
        "info": "INFO",
        "warning": "WARN",
        "error": "ERROR",
        "critical": "CRITICAL",
    }

    def __call__(self, logger: logging.Logger, method: str, event_dict: EventDict) -> EventDict:
        level = event_dict.get("level")

        if isinstance(level, str):
            event_dict["level"] = self.LEVEL_MAP.get(level.lower(), level)

        return event_dict


async def build_processors(container: AsyncContainer) -> list[Processor]:
    sage_config = await container.get(SageConfig)

    timestamp_processor = structlog.processors.TimeStamper(fmt="iso", utc=True, key="@timestamp")
    sage_processor = SageProcessor(sage_config)

    processors: list[Processor] = [
        structlog.processors.add_log_level,
        timestamp_processor,
        sage_processor,
        LevelProcessor(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    return processors


async def configure_logging(container: AsyncContainer) -> None:
    processors = await build_processors(container)
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

    for foreign_logger in ["uvicorn", "uvicorn.access", "uvicorn.asgi", "uvicorn.error", "fastapi", "custom"]:
        logger = logging.getLogger(foreign_logger)
        logger.handlers = [handler]
        logger.propagate = False

    structlog.configure(
        processors=[*processors, structlog.processors.JSONRenderer()],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
