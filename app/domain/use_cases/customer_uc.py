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

    def delete_customer(self, ingredient_id: int) -> str:
        return self.port.delete_customer(ingredient_id)


class CustomerRead(BaseCustomerUseCase):

    def read_customer(self, customer_id: int) -> customer_entity.Customer:
        return self.port.read_customer(customer_id)


class CustomerUpdate(BaseCustomerUseCase):

    def update_customer(self, customer: customer_entity.Customer) -> int:
        return self.port.update_customer(customer)


class CustomerList(BaseCustomerUseCase):

    def list_customer(self, search_key=None, search_value=None):
        return self.port.list_customer(search_key, search_value)
