from pydantic_core import core_schema
from typing import Any
from app.domain.value_objects.base_value_object import ValidateType


class Codebar(ValidateType):

    def __init__(self, code: str):
        self.code = code

    def __str__(self):
        return self.code

    def _check(self):
        """
        Validates the barcode (EAN-13):
        1. Must be 13 digits.
        2. All characters must be numeric.
        3. Must pass EAN-13 checksum validation.
        """
        if not self.code.isdigit():
            return False, "Codebar must contain only numeric characters."

        if len(self.code) != 13:
            return False, "EAN-13 codebar must be exactly 13 digits."

        if not self._validate_ean13_checksum(self.code):
            return False, "Invalid EAN-13 checksum."

        return True, "Codebar is valid."

    def validate(self):
        is_valid, msg = self._check()
        assert is_valid, msg

    def fix(self):
        # No special formatting fix needed; strip whitespace
        self.code = self.code.strip()

    def get(self) -> str:
        return self.code

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls._validate)

    @classmethod
    def _validate(cls, value: Any) -> "Codebar":
        if not isinstance(value, str):
            raise TypeError("Codebar must be a string.")
        bar = cls(value)
        bar.fix()
        bar.validate()
        return bar

    @staticmethod
    def _validate_ean13_checksum(code: str) -> bool:
        """
        Validates the EAN-13 checksum (last digit).
        """
        digits = [int(d) for d in code]
        checksum = digits.pop()  # actual check digit
        total = sum(d if i % 2 == 0 else d * 3 for i, d in enumerate(digits))
        calculated = (10 - (total % 10)) % 10
        return calculated == checksum