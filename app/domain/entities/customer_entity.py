from dataclasses import dataclass

from app.domain.value_objects import document, email, name

@dataclass
class Customer:
       
    document: document.Document
    email: email.Email
    first_name: name.Name
    last_name: name.Name
    id:int=None
