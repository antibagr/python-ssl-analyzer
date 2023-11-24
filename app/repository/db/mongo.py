from loguru import logger
from pymongo.mongo_client import MongoClient

from app.repository.db.base import BaseDB


class MongoDB(BaseDB):
    def __init__(
        self,
        *,
        client: MongoClient,
        database: str,
    ) -> None:
        super().__init__()
        self._client = client
        self._database = self._client[database]

    def is_alive(self) -> bool:
        try:
            self._client.admin.command("ping")
            return True
        except Exception as exc:
            logger.exception(exc)
            return False
