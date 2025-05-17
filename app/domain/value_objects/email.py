from pydantic import BaseModel, Field, field_validator
from validate_email import validate_email


class Email(BaseModel):
    email: str = Field(
        ...,
        description="A valid email address",
        examples=['email@domain.com']
    )

    @field_validator("email")
    def validate(cls, value: str) -> str:
        assert validate_email(value), "Please provide a valid email address"
        return value

    def __str__(self) -> str:
        return self.email

    @property
    def value(self) -> str:
        return self.email
