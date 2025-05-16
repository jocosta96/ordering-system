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