from pydantic import BaseModel, Field, field_validator


class Name(BaseModel):
    name: str = Field(
        ...,
        description="A person's first or last name",
        examples=["Name"]
    )

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        assert value.strip(), "Name cannot be empty"
        return value

    def __str__(self) -> str:
        return self.name

    @property
    def value(self) -> str:
        return self.name
