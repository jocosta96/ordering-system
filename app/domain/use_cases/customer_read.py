from app.domain.ports import customer_read_port
from app.domain.entities import customer_entity

class CustomerCreate:

    def __init__(
        self,
        repository: customer_read_port.ReadUserRepository
    ):
        
        self.user_logon_repository = repository

    def read_user_user(self) -> customer_entity.Customer:
        
        pass