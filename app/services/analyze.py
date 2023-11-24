import typing as t

import attrs
from loguru import logger

from app.dto.entities.fqdn import FQDN
from app.repository.db import DB


class DataProviderRepositoryInterface(t.Protocol):
    def get(self) -> t.Generator[FQDN, None, None]:
        ...


@t.final
@attrs.define(slots=True, frozen=False, kw_only=True)
class AnalyzeService:
    _data_provider_repo: DataProviderRepositoryInterface
    _db: DB

    def analyze(self) -> None:
        logger.info("Starting SSL Checker")
        for fqdn in self._data_provider_repo.get():
            logger.info(f"Adding {fqdn}")
            self._db.save_fqdn(fqdn=fqdn)
