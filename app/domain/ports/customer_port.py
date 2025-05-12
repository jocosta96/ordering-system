import abc

from app.domain.entities import customer_entity


class CustomerRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_customer(self) -> customer_entity.Customer:
        raise NotImplementedError
    
    @abc.abstractmethod
    def read_customer(self) -> customer_entity.Customer:
        raise NotImplementedError
    
    @abc.abstractmethod
    def update_customer(self) -> customer_entity.Customer:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_customer(self) -> customer_entity.Customer:
        raise NotImplementedError