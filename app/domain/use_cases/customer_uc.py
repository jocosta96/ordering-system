from app.domain.ports import customer_port
from app.domain.entities import customer_entity

class BaseCustomerUseCase():

    def __init__(
        self,
        port: customer_port.CustomerPort
    ) -> None:
        self.port = port

class CustomerCreate(BaseCustomerUseCase):

    def create_customer(self, customer: customer_entity.Customer) -> int:
        return self.port.create_customer(customer)


class CustomerDelete(BaseCustomerUseCase):

    def delete_customer(self,seach_key, search_value) -> str:

        key = seach_key.strip().lower()
        if key not in ['id', 'document', 'email']:
            raise ValueError("Invalid search key. Use 'id', 'document', or 'email'.")

        return self.port.delete_customer(seach_key, search_value)
    
class CustomerRead(BaseCustomerUseCase):

    def read_customer(self, seach_key, search_value) -> customer_entity.Customer:

        key = seach_key.strip().lower()

        return self.port.read_customer(key, search_value)
    
class CustomerUpdate(BaseCustomerUseCase):

    def update_customer(self, search_key, search_value, customer: customer_entity.Customer) -> None:

        return self.port.update_customer(search_key, search_value, customer)