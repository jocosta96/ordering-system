from pydantic_core import core_schema
from typing import Any
import re

from app.domain.value_objects.base_value_object import ValidateType

class SKU(ValidateType):

    def __init__(self, sku:str):

        self.sku =  sku

    def __str__(self):

        return self.sku
    
    def _check(self):

        """
        Validates the SKU based on the following rules:
        1. Length should be between 8 and 15 characters.
        2. SKU should be alphanumeric with optional hyphens.
        3. Format: letters, hyphen, numbers, optional hyphen, letters again.
        """
        
        # Rule 1: Length should be between 8 and 15 characters
        if len(self.sku) < 8 or len(self.sku) > 15:
            return False, "SKU length should be between 8 and 15 characters."

        # Rule 2: Valid format using regex - alphanumeric characters with optional hyphens
        pattern = r'^[A-Za-z0-9-]+$'
        if not re.match(pattern, self.sku):
            return False, "SKU should only contain alphanumeric characters and hyphens."
        
        # Rule 3: SKU should follow a general format (e.g., PROD-1234-XYZ)
        # This example regex assumes the format should be letters, a dash, numbers, optional dash, letters
        format_pattern = r'^[A-Za-z]+-\d{4}-[A-Za-z]{3}$'
        if not re.match(format_pattern, self.sku):
            return False, "SKU format should be like 'PROD-1234-XYZ'."
        
        # If all checks pass
        return True, "SKU is valid."
    
    def validate(self):
        assert self._check(), 'please inform a valid sku'

    def fix(self):
        self.sku = self.sku.strip().lower()

    def get(self) -> str:
        return self.sku
    
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        # Define a schema that validates string input and converts to Document
        return core_schema.no_info_plain_validator_function(cls._validate)

    @classmethod
    def _validate(cls, value: Any) -> "SKU":
        if not isinstance(value, str):
            raise TypeError("sku must be a string")
        return cls(value)
