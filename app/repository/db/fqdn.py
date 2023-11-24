from clickhouse_connect.driver.client import Client as ClickHouseClient
from clickhouse_connect.driver.insert import InsertContext
from loguru import logger
from pymongo.mongo_client import MongoClient

from app.dto.entities.collections import FQDNRepository, MongoFQDN
from app.dto.entities.fqdn import FQDN
from app.repository.db.clickhouse import ClickHouseDB
from app.repository.db.mongo import MongoDB


class MongoFQDNDB(MongoDB):
    def __init__(self, *, client: MongoClient, database: str) -> None:
        super().__init__(client=client, database=database)
        self._repository = FQDNRepository(database=self._database)

    def save_fqdn(self, *, fqdn: MongoFQDN) -> None:
        self._repository.save(fqdn)


class ClickHouseFQDNDB(ClickHouseDB):
    def __init__(
        self,
        *,
        client: ClickHouseClient,
        table_name: str,
    ) -> None:
        super().__init__(client=client, table_name=table_name)
        self._context = None

    @property
    def context(self) -> InsertContext:
        if self._context is None:
            self._context = self._client.create_insert_context(
                table=self._table,
                column_names=["fqdn", "alt_names", "supported_protocols"],
            )
        return self._context

    def save_fqdn(self, *, fqdn: FQDN) -> None:
        data = [list(fqdn.model_dump().values())]
        self.context.data = data
        self._client.insert(context=self.context)
