import abc

from app.domain.entities import customer_entity


class ReadUserRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def read_user(self) -> customer_entity.Customer:
        raise NotImplementedError