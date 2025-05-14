from pydantic import BaseModel
from typing import Optional

from app.domain.value_objects import document, email, name


class Customer(BaseModel):

    id: Optional[int] 
    document: str
    email: str
    name: str
    