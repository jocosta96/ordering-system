from app.domain.ports import customer_port
from app.domain.entities import customer_entity
from app.domain.value_objects import document, email

class BaseCustomerUseCase():

    def __init__(
        self,
        port: customer_port.CustomerPort
    ) -> None:
        self.port = port

class CustomerCreate(BaseCustomerUseCase):

    def create_customer(self, customer: customer_entity.Customer) -> int:

        customer.first_name.fix()
        customer.last_name.fix()
        customer.document.fix()
        customer.email.fix()

        customer.first_name.validate()
        customer.last_name.validate()
        customer.document.validate()
        customer.email.validate()

        return self.port.create_customer(customer)


class CustomerDelete(BaseCustomerUseCase):

    def check_customer():
        pass

    def delete_customer(self, customer: customer_entity.Customer) -> int:
        return self.port.delete_customer(customer)
    
class CustomerRead(BaseCustomerUseCase):

    def read_customer(self, seach_key, search_value) -> customer_entity.Customer:

        key = seach_key.strip().lower()
        
        if key == 'document':
            value = document.Document(search_value)

        elif key  == 'email':
            value = email.Email(search_value)

        value.fix()
        value.validate()

        return self.port.read_customer(key, value.get())
    
class CustomerUpdate(BaseCustomerUseCase):

    def update_customer(self, search_key, search_value, customer: customer_entity.Customer) -> None:

        customer.first_name.fix()
        customer.last_name.fix()
        customer.document.fix()
        customer.email.fix()

        customer.first_name.validate()
        customer.last_name.validate()
        customer.document.validate()
        customer.email.validate()

        return self.port.update_customer(search_key, search_value, customer)