import abc


class SQLRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def try_commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_one(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def add_all(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_one(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def list_all(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def list_order_items(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def list_order_item_receipts(self) -> None:
        raise NotImplementedError
