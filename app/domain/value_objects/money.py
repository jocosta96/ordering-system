from decimal import Decimal, ROUND_HALF_EVEN
from pydantic import BaseModel, Field, field_validator
from typing import Union


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
    
    @staticmethod
    def _format(value: Decimal) -> str:
        """
        Formats the amount to a string with 2 decimal places.
        """
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)

    def __str__(self) -> str:
        return str(self._format(self.amount))
    
    @property
    def value(self) -> float:
        return float(self._format(self.amount))
    
    def __add__(self, other: 'Money') -> 'Money':
        return self._format(value=Decimal(self.amount) + Decimal(other.amount))
