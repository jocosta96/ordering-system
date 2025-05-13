from validate_email import validate_email

from app.domain.types.type_validation import ValidateType

class Email(ValidateType):

    def __init__(self, email:str):

        self.email =  email
    
    def validate(self):
        assert validate_email(self.email), 'please inform a valid email address'