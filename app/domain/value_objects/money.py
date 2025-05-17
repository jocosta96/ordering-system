from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pydantic_core import core_schema
from typing import Any

from app.domain.value_objects.base_value_object import ValidateType

class Money(ValidateType, Decimal):

    def __init__(self, amount: Decimal):
        self.amount = amount

    def __str__(self):
        return f"{self.amount:.2f}"
    
    def __float__(self):
        return float(self.amount)
    
    def _check(self):
        """
        Validates the money value:
        1. Must be a valid Decimal.
        2. Must be non-negative.
        3. Must have at most 2 decimal places.
        """
        if self.amount < 0:
            return False, "Amount must be non-negative."

        # Check for up to 2 decimal places
        if self.amount.as_tuple().exponent < -2:
            return False, "Amount must have at most 2 decimal places."

        return True, "Amount is valid."

    def validate(self):
        is_valid, msg = self._check()
        assert is_valid, msg

    def fix(self):
        # Round to 2 decimal places using ROUND_HALF_UP (standard financial rounding)
        self.amount = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get(self) -> Decimal:
        return self.amount

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls._validate)

    @classmethod
    def _validate(cls, value: Any) -> "Money":
        try:
            if isinstance(value, (float, int, str)):
                value = Decimal(str(value))
            elif not isinstance(value, Decimal):
                raise TypeError("Money value must be a float")
        except (InvalidOperation, ValueError):
            raise ValueError("Invalid format for money amount")

        money = cls(value)
        money.fix()
        money.validate()
        return money
