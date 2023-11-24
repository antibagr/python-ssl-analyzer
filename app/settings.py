import pathlib
import typing as t

from pydantic_settings import BaseSettings, SettingsConfigDict


@t.final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    TEST_SSL_CONTAINER_NAME: str
    TEST_SSL_OUTPUT_DIR: pathlib.Path
    TEST_SSL_COMMANDS_FILE: pathlib.Path
    TEST_SSL_WORKDIR: pathlib.Path

    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str
    CLICKHOUSE_TABLE_NAME: str
    CLICKHOUSE_CONNECT_TIMEOUT: int = 15


settings = Settings(_env_file=".env")  # type: ignore[call-arg]
