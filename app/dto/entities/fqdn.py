import typing as t

from pydantic import ConfigDict, Field, field_serializer

from app.dto.annotations import Domain
from app.dto.entities.base import BaseModel


@t.final
class FQDN(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    fqdn: str = Field(..., alias="fqdn")
    alt_names: set[Domain] = Field(..., alias="alt_names", default_factory=set)
    supported_protocols: list[str] = Field(..., alias="supported_protocols", default_factory=list)

    @field_serializer("alt_names")
    def serialize_alt_names(self, value: set[Domain]) -> list[str]:
        return list(value)
