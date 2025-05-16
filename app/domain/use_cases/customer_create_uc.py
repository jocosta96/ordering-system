from app.domain.use_cases import customer_base_uc
from app.domain.entities import customer_entity


class CustomerCreate(customer_base_uc.BaseCustomerUseCase):

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
