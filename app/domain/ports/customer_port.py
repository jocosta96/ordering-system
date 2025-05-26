import abc

from app.domain.entities import customer_entity


class CustomerPort(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_customer(self, customer: customer_entity.Customer) -> customer_entity.Customer:
        raise NotImplementedError

    @abc.abstractmethod
    def read_customer(self, customer_id: int) -> customer_entity.Customer:
        raise NotImplementedError

    @abc.abstractmethod
    def update_customer(self, customer: customer_entity.Customer) -> customer_entity.Customer:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_customer(self, ingredient_id: int) -> customer_entity.Customer:
        raise NotImplementedError

    @abc.abstractmethod
    def list_customer(self, search_key=None, search_value=None):
        raise NotImplementedError
