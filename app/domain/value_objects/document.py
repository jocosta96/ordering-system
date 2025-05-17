import re
from pydantic import BaseModel, Field, field_validator


class Document(BaseModel):
    document: str = Field(
        ...,
        description="Brazilian CPF number with 11 digits",
        examples=['83904593021']
    )

    @field_validator("document")
    def validate_cpf(cls, value: str) -> str:
        assert re.fullmatch(r"\d{11}", value), "CPF must have exactly 11 digits"
        numbers = [int(d) for d in value]
        sum1 = sum(a * b for a, b in zip(numbers[:9], range(10, 1, -1)))
        sum2 = sum(a * b for a, b in zip(numbers[:10], range(11, 1, -1)))

        assert numbers[9] == ((sum1 * 10 % 11) % 10), "Invalid CPF (first check digit)"
        assert numbers[10] == ((sum2 * 10 % 11) % 10), "Invalid CPF (second check digit)"
        return value

    def __str__(self) -> str:
        return self.document

    @property
    def value(self) -> str:
        return self.document
