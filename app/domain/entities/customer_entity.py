from app.domain.value_objects.document import Document
from app.domain.value_objects.email import Email
from app.domain.value_objects.name import Name

class Customer:

    def __init__(
        self,
        document: Document,
        email: Email,
        first_name: Name,
        last_name: Name,
        id: int = None
    ):
        
        self.document = document
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.id=id
