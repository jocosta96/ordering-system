import abc

class ValidateType(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def validate():
        raise NotImplementedError