import abc

from app.domain.entities import customer_entity


class CreateUserRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_user(self) -> customer_entity.Customer:
        raise NotImplementedError
    
    @abc.abstractmethod
    def read_user(self) -> customer_entity.Customer:
        raise NotImplementedError