import pydantic


class BaseModel(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
    )

    @property
    def is_empty(self) -> bool:
        return None in self.model_dump(warnings=False).values()
