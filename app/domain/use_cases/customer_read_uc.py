from app.domain.use_cases import customer_base_uc
from app.domain.entities import customer_entity

class CustomerRead(customer_base_uc.BaseCustomerUseCase):

    def read_customer(self, customer: customer_entity.Customer) -> int:
        return self.customer_base_uc.port.read_customer(customer)