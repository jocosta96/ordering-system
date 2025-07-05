import abc

from app.domain.entities import product_entity


class ProductPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_product(self) -> product_entity.Product:
        raise NotImplementedError

    @abc.abstractmethod
    def read_product(self) -> product_entity.Product:
        raise NotImplementedError

    @abc.abstractmethod
    def update_product(self) -> product_entity.Product:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_product(self) -> product_entity.Product:
        raise NotImplementedError

    @abc.abstractmethod
    def restore_deleted_product(self) -> product_entity.Product:
        raise NotImplementedError

    @abc.abstractmethod
    def list_product(self) -> list[product_entity.Product]:
        raise NotImplementedError
