from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class Money(BaseModel):
    amount: Decimal = Field(..., description="Amount of Money in BRL")

    @field_validator('amount')
    def validate(cls, values):
        """
        Validates the money value:
        1. Must be a valid Decimal.
        2. Must be non-negative.
        3. Must have at most 2 decimal places.
        """
        assert values >= 0, "Amount must be non-negative."
        normalized = values.normalize()
        decimal_places = -normalized.as_tuple().exponent if normalized.as_tuple().exponent < 0 else 0
        assert decimal_places <= 2, "Amount must have at most 2 decimal places."

        return values

    def __float__(self) -> float:
        return round(self.amount, 2)

    @property
    def value(self) -> float:
        return round(self.amount, 2)
