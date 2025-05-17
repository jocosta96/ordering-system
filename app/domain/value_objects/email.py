from pydantic_core import core_schema
from typing import Any
from validate_email import validate_email

from app.domain.value_objects.base_value_object import ValidateType

class Email(ValidateType):

    def __init__(self, email:str):

        self.email =  email

    def __str__(self):

        return self.email
    
    def validate(self):
        assert validate_email(self.email), 'please inform a valid email address'

    def fix(self):
        self.email = self.email.strip().lower()

    def get(self) -> str:
        return self.email
    
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        # Define a schema that validates string input and converts to Document
        return core_schema.no_info_plain_validator_function(cls._validate)

    @classmethod
    def _validate(cls, value: Any) -> "Email":
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        return cls(value)