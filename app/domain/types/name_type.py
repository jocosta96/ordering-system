from app.domain.types.type_validation import ValidateType

class Name(ValidateType):

    def __init__(self, first_name:str, last_name:str) -> None:

        self.first_name =  first_name
        self.last_name = last_name
    
    def validate(self):
        
        assert bool(self.first_name) and bool(self.last_name), 'Need first name and last name'
