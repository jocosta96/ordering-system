from app.domain.ports import customer_create_port
from app.domain.entities import customer_entity

class CustomerCreate:

    def __init__(
        self,
        repository: customer_create_port.CreateUserRepository
    ):
        
        self.user_logon_repository = repository

    def create_user(self, logon=customer_entity.Customer):
        
        pass