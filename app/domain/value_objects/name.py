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