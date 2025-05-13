from app.domain.use_cases import customer_base_uc
from app.domain.entities import customer_entity
from app.domain.types import email_type, document_type, name_type


class CustomerCreate(customer_base_uc.BaseCustomerUseCase):

    def create(self, customer: customer_entity.Customer) -> int:

        name_type.Name(customer.first_name, customer.last_name).validate()
        document_type.Document(customer.document).validate()
        email_type.Email(customer.email).validate()

        return self.customer_base_uc.port.create_customer(customer)
