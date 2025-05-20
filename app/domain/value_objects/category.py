from pydantic import BaseModel, Field, field_validator
from enum import Enum


class ProductCategoryType(str, Enum):

    LANCHE = "LANCHE"
    ACOMPANHAMENTO = "ACOMPANHAMENTO"
    BEBIDA = "BEBIDA"
    SOBREMESA = "SOBREMESA"


class ProductCategory(BaseModel):

    category: str = Field(
        ...,
        description="Product Category",
        examples=["LANCHE", "ACOMPANHAMENTO", "BEBIDA", "SOBREMESA"]
    )

    @field_validator("category")
    def validate(cls, value):
        assert ProductCategoryType(value)
        return value
    
    def __str__(self) -> str:
        return self.category

    @property
    def value(self) -> str:
        return self.category

