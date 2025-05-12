from app.domain.ports import customer_port

class BaseCustomerUseCase():

    def __init__(
        self,
        repository: customer_port.CustomerRepository
    ) -> None:
        self.repository = repository