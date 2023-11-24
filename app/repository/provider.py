import pathlib
import typing as t

import attrs
from loguru import logger

from app.dto.entities.fqdn import FQDN
from app.lib.docker import TestSSLContainer
from app.lib.test_ssl_parser import TestSSLJsonParser


@t.final
@attrs.define(slots=True, frozen=False, kw_only=True)
class TestSSLDataProviderRepository:
    _container: TestSSLContainer
    _json_parser: TestSSLJsonParser
    _input_path: pathlib.Path

    def get_missing_fqdn(self, *, parsed: list[str]) -> t.Generator[str, None, None]:
        for line in self._input_path.read_text().splitlines():
            try:
                host, _ = line.split(":")
            except ValueError:
                logger.error(f"Incorrect input line: {line}")
                continue
            if host not in parsed:
                yield host

    def get(self) -> t.Generator[FQDN, None, None]:
        self._container.wait_for_complete()
        self._json_parser.set_data(data=self._container.get_json())

        fqdn_list = []

        try:
            for fqdn in self._json_parser.parse():
                fqdn_list.append(fqdn.fqdn)
                yield fqdn
        finally:
            for missing_fqdn in self.get_missing_fqdn(parsed=fqdn_list):
                logger.error(f"Failed to parse {missing_fqdn}")
