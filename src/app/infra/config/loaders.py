from adaptix import Retort

from app.infra.config.models import ServerConfigModel
from app.infra.config.sources import EnvSource
from app.presentation.api.config.models import ServerConfig

retort = Retort()


class BaseEnvLoader:
    def __init__(self, source: EnvSource) -> None:
        self._source = source


class EnvServerConfigLoader(BaseEnvLoader):
    def load(self) -> ServerConfig:
        raw_data = self._source.get_present_values(["SERVER_WORKERS", "SERVER_HOST", "SERVER_PORT"])
        validated = ServerConfigModel.model_validate(raw_data).model_dump()

        return retort.load(validated, ServerConfig)
