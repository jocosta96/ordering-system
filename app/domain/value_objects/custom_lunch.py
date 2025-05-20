from pydantic import BaseModel, Field, field_validator
from enum import Enum


class CustomLunchType(str, Enum):

    LANCHE = "LANCHE"
    BEBIDA = "BEBIDA"
    ACOMPANHAMENTO = "ACOMPANHAMENTO"
    SOBREMESA = "SOBREMESA"


class CustomLunchType(BaseModel):

    custom_lunch: str = Field(
        ...,
        description="Custom Lunch Type",
        examples=["LANCHE", "BEBIDA", "ACOMPANHAMENTO", "SOBREMESA"]
    )

    @field_validator("custom_lunch")
    def validate(cls, value):
        assert CustomLunchType(value)
        return value
    
    def __str__(self) -> str:
        return self.custom_lunch

    @property
    def value(self) -> str:
        return self.custom_lunch

