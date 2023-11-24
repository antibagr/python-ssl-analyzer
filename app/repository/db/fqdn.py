from clickhouse_connect.driver.client import Client as ClickHouseClient
from clickhouse_connect.driver.insert import InsertContext

from app.dto.entities.fqdn import FQDN
from app.repository.db.clickhouse import ClickHouseDB


class ClickHouseFQDNDB(ClickHouseDB):
    def __init__(
        self,
        *,
        client: ClickHouseClient,
        table_name: str,
    ) -> None:
        super().__init__(client=client, table_name=table_name)
        self._context: InsertContext = None  # type: ignore

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
