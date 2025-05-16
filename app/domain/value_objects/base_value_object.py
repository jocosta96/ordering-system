import abc

class ValidateType(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def validate():
        raise NotImplementedError
    
    @abc.abstractmethod
    def fix():
        raise NotImplementedError
    
    @abc.abstractmethod
    def get():
        raise NotImplementedError