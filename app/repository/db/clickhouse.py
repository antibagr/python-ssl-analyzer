from clickhouse_connect.driver.client import Client as ClickHouseClient

from app.repository.db.base import BaseDB


class ClickHouseDB(BaseDB):
    def __init__(
        self,
        *,
        client: ClickHouseClient,
        table_name: str,
    ) -> None:
        super().__init__()
        self._client = client
        self._table = table_name

    def connect(self) -> None:
        self._client.command(
            """CREATE TABLE IF NOT EXISTS {table:Identifier} (
                `fqdn` String,
                `alt_names` Array(String),
                `supported_protocols` Array(String)
            )
            ENGINE = ReplacingMergeTree
            PRIMARY KEY (fqdn)
            ORDER BY (fqdn);
        """,
            parameters={"table": self._table},
        )

    def disconnect(self) -> None:
        self._client.close()

    def is_alive(self) -> bool:
        return self._client.ping()
