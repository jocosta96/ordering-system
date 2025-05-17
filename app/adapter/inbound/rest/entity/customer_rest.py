from pydantic import BaseModel
from typing import Optional

from app.domain.value_objects import document, email, name


class Customer(BaseModel):

    id: Optional[int] 
    document: Optional[document.Document]
    email: Optional[email.Email]
    first_name: name.Name
    last_name: name.Name
    