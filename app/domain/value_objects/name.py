from pydantic_core import core_schema
from typing import Any
from app.domain.value_objects.base_value_object import ValidateType

class Name(ValidateType):

    def __init__(self, name:str) -> None:

        self.name = name
    
    def __str__(self):

        return self.name
    
    def validate(self):
        
        assert self.name, 'Name can not be empty'

    def fix(self):

        self.name =  self.name.strip().upper()

    def get(self) -> str:

        return self.name

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        # Define a schema that validates string input and converts to Document
        return core_schema.no_info_plain_validator_function(cls._validate)

    @classmethod
    def _validate(cls, value: Any) -> "Name":
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        return cls(value)