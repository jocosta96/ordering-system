from app.domain.ports import customer_port

class BaseCustomerUseCase():

    def __init__(
        self,
        port: customer_port.CustomerPort
    ) -> None:
        self.port = port