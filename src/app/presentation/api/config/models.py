from dataclasses import dataclass


@dataclass(frozen=True)
class ServerConfig:
    host: str
    port: int
    workers: int


@dataclass(frozen=True)
class PostgresConfig:
    host: str
    port: int
    user: str
    password: str
    db: str
