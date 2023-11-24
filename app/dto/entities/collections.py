import typing as t

from pydantic_mongo import AbstractRepository

from app.dto.entities.base import ObjectId
from app.dto.entities.fqdn import FQDN


# @t.final
class MongoFQDN(FQDN):
    id: ObjectId = None


class FQDNRepository(AbstractRepository[MongoFQDN]):
    class Meta:
        collection_name = "fqdns"
