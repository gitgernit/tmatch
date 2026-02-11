from typing import Final

from sqlalchemy import MetaData
from sqlalchemy.orm import registry

meta_data: Final = MetaData()
mapper_registry: Final = registry()
