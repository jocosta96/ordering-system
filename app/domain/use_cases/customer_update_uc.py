from app.domain.use_cases import customer_base_uc
from app.domain.entities import customer_entity

class CustomerUpdate(customer_base_uc.BaseCustomerUseCase):

    def update(self, customer: customer_entity.Customer) -> int:
        return self.customer_base_uc.repository.update_customer(customer)