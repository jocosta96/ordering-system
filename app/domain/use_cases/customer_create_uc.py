from app.domain.use_cases import customer_base_uc
from app.domain.entities import customer_entity
from app.domain.value_objects import document, email, name


class CustomerCreate(customer_base_uc.BaseCustomerUseCase):

    def create(self, customer: customer_entity.Customer) -> int:

        name.Name(customer.first_name, customer.last_name).validate()
        document.Document(customer.document).validate()
        email.Email(customer.email).validate()

        return self.customer_base_uc.port.create_customer(customer)
