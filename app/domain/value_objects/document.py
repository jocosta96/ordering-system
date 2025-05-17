from pydantic_core import core_schema
from typing import Any
import re

from app.domain.value_objects.base_value_object import ValidateType

class Document(ValidateType):

    def __init__(self, document: str) -> None:
        if not isinstance(document, str):
            raise TypeError(f"Document must be initialized with a string, got {type(document).__name__}")


        self.document = document
        self.fix()
        self.validate()

    def __str__(self) -> str:
        return self.document

    def check_document(self) -> bool:
        import re
        if not re.match(r'\d{11}', self.document):
            return False
        numbers = [int(digit) for digit in self.document]
        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False
        sum1 = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        if numbers[9] != ((sum1 * 10 % 11) % 10):
            return False
        sum2 = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        if numbers[10] != ((sum2 * 10 % 11) % 10):
            return False
        return True

    def validate(self) -> None:
        assert self.check_document(), 'Please review your document number'

    def fix(self) -> None:
        import re
        self.document = re.sub(r"\W", "", self.document).strip()

    def get(self) -> str:
        return self.document

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls._validate)

    @classmethod
    def _validate(cls, value: Any) -> "Document":
        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            raise TypeError("Document must be a string")
        return cls(value)