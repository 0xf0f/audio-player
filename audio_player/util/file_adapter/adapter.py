from abc import ABC, abstractmethod
from ..adapters import Adapter


class FileAdapter(Adapter, ABC):
    supported_extensions = ()
    supports_urls = False

    def __init__(self, path: str):
        Adapter.__init__(self)
        self.path = path

    @classmethod
    @abstractmethod
    def adapt(cls, path: str):
        pass

    @classmethod
    def open(cls, path: str):
        """
        Convenience alias for adapt.
        """
        return cls.adapt(path)
