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


@dataclass(frozen=True)
class AccessTokenConfig:
    crypto_key: str
    expires_in_seconds: int


@dataclass(frozen=True)
class YandexOAuthConfig:
    client_id: str
    client_secret: str


@dataclass(frozen=True)
class OpentelemetryConfig:
    traces_exporter: str
    exporter_otlp_endpoint: str
    service_name: str
