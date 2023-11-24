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

    ENVIRONMENT: str
    DEBUG: bool

    TEST_SSL_CONTAINER_NAME: str
    TEST_SSL_OUTPUT_FILE: pathlib.Path
    TEST_SSL_INPUT_FILE: pathlib.Path
    TEST_SSL_DATA_DIR: pathlib.Path

    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int
    CLICKHOUSE_USER: str
    CLICKHOUSE_PASSWORD: str
    CLICKHOUSE_TABLE_NAME: str

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "prod"


settings = Settings(_env_file=".env")  # type: ignore[call-arg]
