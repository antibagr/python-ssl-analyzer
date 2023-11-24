import typing as t

from loguru import logger

from app.dto.annotations import Domain, TestSSLRecords
from app.dto.entities.fqdn import FQDN
from app.dto.exceptions import TestSSLScanError

Protocols: t.Final = ("SSLv2", "SSLv3", "TLS1", "TLS1_1", "TLS1_2", "TLS1_3")


class TestSSLJsonParser:
    @staticmethod
    def parse(*, data: TestSSLRecords) -> FQDN:
        fqdns: dict[str, FQDN] = {}

        for record in data:
            logger.bind(ip=record["ip"])

            try:
                fqdn = record["ip"].split("/")[0]
            except Exception as exc:
                raise TestSSLScanError(f"Failed to parse FQDN from {record['ip']}: {exc}") from exc

            if not fqdn:
                continue

            if fqdn not in fqdns:
                fqdns[fqdn] = FQDN(fqdn=fqdn)

            if record["id"] == "scanProblem" and record["severity"] == "FATAL":
                raise TestSSLScanError(record["finding"])

            if record["id"] in Protocols:
                if record["finding"] != "not offered":
                    fqdns[fqdn].supported_protocols.append(record["id"])
            elif record["id"].startswith("cert_subjectAltName"):
                fqdns[fqdn].alt_names |= set(t.cast(list[Domain], record["finding"].split()))

        if len(fqdns) != 1:
            raise TestSSLScanError("Multiple FQDNs found in scan results")

        return list(fqdns.values())[0]
