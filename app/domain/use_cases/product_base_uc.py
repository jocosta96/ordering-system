from app.domain.ports import product_port


class BaseProductUseCase():

    def __init__(
        self,
        port: product_port.ProductPort
    ) -> None:
        self.port = port
