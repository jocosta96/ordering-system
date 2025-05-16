from app.domain.use_cases import customer_base_uc
from app.domain.entities import customer_entity
from app.domain.value_objects import document, email, name


class CustomerUpdate( customer_base_uc.BaseCustomerUseCase):

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