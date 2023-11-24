import typing as t

from loguru import logger

from app.dto.annotations import Domain, TestSSLRecords
from app.dto.entities.fqdn import FQDN

Protocols: t.Final = ("SSLv2", "SSLv3", "TLS1", "TLS1_1", "TLS1_2", "TLS1_3")


class TestSSLJsonParser:
    def __init__(self) -> None:
        self._data: TestSSLRecords = []

    def set_data(self, *, data: TestSSLRecords) -> None:
        self._data = data

    def parse(self) -> t.Iterable[FQDN]:
        fqdns: dict[str, FQDN] = {}

        for record in self._data:
            logger.bind(ip=record["ip"])

            try:
                fqdn = record["ip"].split("/")[0]
            except Exception as exc:
                logger.warning(f"Failed to parse FQDN from {record['ip']}: {exc}")
                continue

            if not fqdn:
                continue

            if fqdn not in fqdns:
                fqdns[fqdn] = FQDN(fqdn=fqdn)

            if record["id"] in Protocols:
                if record["finding"] != "not offered":
                    fqdns[fqdn].supported_protocols.append(record["id"])
            elif record["id"].startswith("cert_subjectAltName"):
                fqdns[fqdn].alt_names |= set(t.cast(list[Domain], record["finding"].split()))

        return iter(fqdns.values())
