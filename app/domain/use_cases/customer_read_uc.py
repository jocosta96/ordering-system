from app.domain.use_cases import customer_base_uc
from app.domain.entities import customer_entity

class CustomerRead(customer_base_uc.BaseCustomerUseCase):

    def create(self, customer: customer_entity.Customer) -> int:
        return self.customer_base_uc.repository.read_customer(customer)