from app.domain.use_cases import customer_base_uc
from app.domain.entities import customer_entity
from app.domain.value_objects import document, email

class CustomerRead(customer_base_uc.BaseCustomerUseCase):

    def read_customer(self, seach_key, search_value) -> customer_entity.Customer:

        key = seach_key.strip().lower()
        
        if key == 'document':
            value = document.Document(search_value)

        elif key  == 'email':
            value = email.Email(search_value)

        value.fix()
        value.validate()

        return self.port.read_customer(key, value.get())