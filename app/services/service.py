import typing as t
from contextlib import contextmanager

import clickhouse_connect
import docker
from loguru import logger
from pymongo.mongo_client import MongoClient

from app.lib.docker import TestSSLContainer
from app.lib.test_ssl_parser import TestSSLJsonParser
from app.repository.db import DB
from app.repository.provider import TestSSLDataProviderRepository
from app.services.ssl_checker import SSLCheckerService
from app.settings import settings

# Dependency Layer
docker_client = docker.from_env()
clickhouse_client = clickhouse_connect.get_client(
    host=settings.CLICKHOUSE_HOST,
    port=settings.CLICKHOUSE_PORT,
    user=settings.CLICKHOUSE_USER,
    password=settings.CLICKHOUSE_PASSWORD,
    secure=False,
    connect_timeout=15,
)

test_ssl_parser = TestSSLJsonParser()
test_ssl_container = TestSSLContainer(
    client=docker_client,
    container_name=settings.TEST_SSL_CONTAINER_NAME,
    output_path=settings.TEST_SSL_DATA_DIR / settings.TEST_SSL_OUTPUT_FILE,
)

# Repository Layer
db = DB(client=clickhouse_client, table_name=settings.CLICKHOUSE_TABLE_NAME)
data_provider_repo = TestSSLDataProviderRepository(
    container=test_ssl_container,
    json_parser=test_ssl_parser,
    input_path=settings.TEST_SSL_DATA_DIR / settings.TEST_SSL_INPUT_FILE,
)


# Service Layer
ssl_checker_service = SSLCheckerService(
    data_provider_repo=data_provider_repo,
    db=db,
)


def startup() -> None:
    logger.info("starting up")
    logger.info(f"database status: {db.is_alive()}")
    db.connect()
    from app.dto.entities.fqdn import FQDN

    db.save_fqdn(
        fqdn=FQDN(
            fqdn="test.com",
            alt_names=["test.com", "test2.com"],
            supported_protocols=["TLSv1.2", "TLSv1.3"],
        )
    )


def shutdown() -> None:
    logger.info("shutting down")
    test_ssl_container.stop()
    db.disconnect()


@contextmanager
def application_dependencies() -> t.Generator[None, None, None]:
    startup()
    try:
        yield
    finally:
        shutdown()
