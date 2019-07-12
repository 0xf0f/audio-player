from abc import ABC, abstractmethod
from .exceptions import UnableToAdapt


class Adapter(ABC):
    @classmethod
    @abstractmethod
    def adapt(cls, *args, **kwargs):
        raise UnableToAdapt
