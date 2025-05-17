from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.domain.value_objects import document, email, name


class Customer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: Optional[int] 
    document: Optional[document.Document]
    email: Optional[email.Email]
    first_name: name.Name
    last_name: name.Name
    