from pydantic import BaseModel #da fast api
from typing import Optional

class Customer(BaseModel):
    #dataclass

    id: Optional[int] 
    document: str
    email: str
    name: str #implementar classes especializadas para nome e mail