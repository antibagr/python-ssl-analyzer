import datetime as dt

import pydantic


class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        json_encoders={
            dt.datetime: dt.datetime.isoformat,
            set: list,
        },
    )

    @property
    def is_empty(self) -> bool:
        return None in self.model_dump(warnings=False).values()
