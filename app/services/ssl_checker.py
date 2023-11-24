import typing as t

import attrs
import docker
from loguru import logger

from app.dto.entities.fqdn import FQDN
from app.repository.db import DB

logger.bind(context="ssl_checker")


class DataProviderRepositoryInterface(t.Protocol):
    def get(self) -> t.Generator[FQDN, None, None]:
        ...


@t.final
@attrs.define(slots=True, frozen=False, kw_only=True)
class SSLCheckerService:
    _data_provider_repo: DataProviderRepositoryInterface
    _db: DB

    def run(self) -> None:
        logger.info("running ssl checker")
        for fqdn in self._data_provider_repo.get():
            logger.info(f"Adding {fqdn}")
            self._db.save_fqdn(fqdn=fqdn)
