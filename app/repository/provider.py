import typing as t

import attrs
from loguru import logger

from app.dto.entities.fqdn import FQDN
from app.dto.exceptions import TestSSLScanError
from app.lib.testssl import TestSSLContainer, TestSSLJsonParser


@t.final
@attrs.define(slots=True, frozen=False, kw_only=True)
class TestSSLDataProviderRepository:
    _container: TestSSLContainer
    _json_parser: TestSSLJsonParser

    def get(self) -> t.Generator[FQDN, None, None]:
        self._container.wait_for_complete()

        for data in self._container.stream_data():
            try:
                yield self._json_parser.parse(data=data)
            except TestSSLScanError as exc:
                logger.error(f"Failed to parse data: {exc}")
