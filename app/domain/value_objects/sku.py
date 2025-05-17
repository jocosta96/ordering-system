from pydantic import BaseModel, Field, field_validator
import re

class SKU(BaseModel):
    
    sku: str = Field(..., description="Stock Keeping Unit")

    @field_validator('sku')
    def _check(cls, values):

        """
        Validates the SKU based on the following rules:
        1. Length should be between 8 and 15 characters.
        2. SKU should be alphanumeric with optional hyphens.
        3. Format: letters, hyphen, numbers, optional hyphen, letters again.
        """
        
        assert len(values) > 8 or len(values) < 15, "SKU length error"

        pattern = r'^[A-Za-z0-9-]+$'
        assert re.match(pattern, values), "Invalid Characteres Detected"
        
        format_pattern = r'^[A-Za-z]+-\d{4}-[A-Za-z]{3}$'
        assert re.match(format_pattern, values), "SKU format should be like 'PROD-1234-XYZ'."

        return values

    def __str__(self) -> str:
        return self.sku

    @property
    def value(self) -> str:
        return self.sku
