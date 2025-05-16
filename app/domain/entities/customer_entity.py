from app.domain.value_objects.document import Document
from app.domain.value_objects.email import Email
from app.domain.value_objects.name import Name

class Customer:

    def __init__(
        self,
        document:str,
        email:str,
        first_name:str,
        last_name:str,
        id:int=None
    ):
        
        self.document = Document(document)
        self.email = Email(email)
        self.first_name = Name(first_name)
        self.last_name = Name(last_name)
        self.id=id
