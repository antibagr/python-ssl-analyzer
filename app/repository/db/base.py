import types
import typing as t

from loguru import logger
from pymongo.mongo_client import MongoClient

from app.settings import settings


class BaseDB:
    def __enter__(self) -> t.Self:
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException],
        _value: BaseException,
        _traceback: types.TracebackType,
    ) -> None:
        ...

    def connect(self) -> None:
        logger.bind(context=self.__class__.__name__).info("database_connected")

    def disconnect(self) -> None:
        logger.bind(context=self.__class__.__name__).info("database_disconnected")

    def is_alive(self) -> bool:
        return True
