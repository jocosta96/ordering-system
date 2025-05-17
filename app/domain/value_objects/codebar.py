from pydantic import BaseModel, Field, field_validator


class Codebar(BaseModel):
    code: str = Field(..., description="EAN-13 Codebar")

    @field_validator("code")
    def validate(cls, value):
        """
        Validates the barcode (EAN-13):
        1. Must be 13 digits.
        2. All characters must be numeric.
        3. Must pass EAN-13 checksum validation.
        """

        assert value.isdigit(), "Codebar must contain only numeric characters."

        assert len(value) == 13, "EAN-13 codebar must be exactly 13 digits."
        
        digits = [int(d) for d in value]
        checksum = digits.pop()  # actual check digit
        total = sum(d if i % 2 == 0 else d * 3 for i, d in enumerate(digits))
        calculated = (10 - (total % 10)) % 10

        assert calculated == checksum, "Invalid EAN-13 checksum."

        return value
    
    def __str__(self) -> str:
        return self.code

    @property
    def value(self) -> str:
        return self.code

