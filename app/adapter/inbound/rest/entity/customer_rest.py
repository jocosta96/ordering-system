from pydantic import BaseModel
from typing import Optional

from app.domain.value_objects import document, email, name


class Customer(BaseModel):
    id: Optional[int] = None
    document: Optional[document.Document]
    email: Optional[email.Email]
    first_name: name.Name = ""
    last_name: name.Name = ""

    model_config = {
        "arbitrary_types_allowed": True,
        "json_schema_extra": {
            "example": {
                "document": {"document": "83904593021"},
                "email": {"email": "email@domain.com"},
                "first_name": {"name": "PRIM"},
                "last_name": {"name": "SEC"},
            }
        },
    }
