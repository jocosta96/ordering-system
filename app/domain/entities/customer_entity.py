from dataclasses import dataclass

@dataclass
class Customer:
       
    document: str
    email: str
    first_name: str
    last_name: str
    id:int=None
