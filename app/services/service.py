import typing as t
from contextlib import contextmanager

import clickhouse_connect
import docker
from loguru import logger

from app.lib.testssl import TestSSLContainer, TestSSLJsonParser
from app.repository.db import DB
from app.repository.provider import TestSSLDataProviderRepository
from app.services.analyze import AnalyzeService
from app.settings import settings

# Dependency Layer
docker_client = docker.from_env()
clickhouse_client = clickhouse_connect.get_client(
    host=settings.CLICKHOUSE_HOST,
    port=settings.CLICKHOUSE_PORT,
    user=settings.CLICKHOUSE_USER,
    password=settings.CLICKHOUSE_PASSWORD,
    secure=False,
    connect_timeout=settings.CLICKHOUSE_CONNECT_TIMEOUT,
)

test_ssl_parser = TestSSLJsonParser()
test_ssl_container = TestSSLContainer(
    client=docker_client,
    container_name=settings.TEST_SSL_CONTAINER_NAME,
    workdir=settings.TEST_SSL_WORKDIR,
    output_directory=settings.TEST_SSL_OUTPUT_DIR,
    commands_file_name=settings.TEST_SSL_COMMANDS_FILE,
)

# Repository Layer
db = DB(client=clickhouse_client, table_name=settings.CLICKHOUSE_TABLE_NAME)
data_provider_repo = TestSSLDataProviderRepository(
    container=test_ssl_container,
    json_parser=test_ssl_parser,
)


# Service Layer
analyze_service = AnalyzeService(
    data_provider_repo=data_provider_repo,
    db=db,
)


def startup() -> None:
    logger.info("Starting up")
    db.connect()


def shutdown() -> None:
    logger.info("Shutting down")
    test_ssl_container.stop()
    db.disconnect()


@contextmanager
def application_dependencies() -> t.Generator[None, None, None]:
    startup()
    try:
        yield
    finally:
        shutdown()
