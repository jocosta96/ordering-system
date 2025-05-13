from app.domain.use_cases import customer_base_uc
from app.domain.entities import customer_entity

class CustomerDelete(customer_base_uc.BaseCustomerUseCase):

    def check_customer():
        pass

    def delete(self, customer: customer_entity.Customer) -> int:
        return self.customer_base_uc.port.delete_customer(customer)