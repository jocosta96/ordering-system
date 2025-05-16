import re

from app.domain.value_objects.base_value_object import ValidateType

class Document(ValidateType):

    def __init__(self, document: str) -> None:
         
        self.document = document

    def __str__(self):

        return self.document

    def check_document(self) -> bool:

        if not re.match(r'\d{11}', self.document):
            return False

        numbers = [int(digit) for digit in self.document]

        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True
    
    def validate(self) -> None:
        assert self.check_document(), 'Please review your document number'

    def fix(self) -> None:

        self.document = re.sub(r"\W", "", self.document).strip()

    def get(self) -> str:

        return self.document