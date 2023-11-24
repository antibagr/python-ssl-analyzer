from __future__ import annotations

import datetime as dt
import typing as t

import bson
import pydantic
from bson.errors import InvalidId


class ObjectId(bson.ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: t.Any) -> ObjectId:
        try:
            return cls(v)
        except InvalidId as exc:
            raise ValueError(f"{v} is not a valid ObjectId") from exc


class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        json_encoders={
            dt.datetime: dt.datetime.isoformat,
            ObjectId: str,
            set: list,
        },
    )

    @property
    def is_empty(self) -> bool:
        return None in self.model_dump(warnings=False).values()
