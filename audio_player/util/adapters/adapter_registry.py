from .adapter import Adapter
from .exceptions import UnableToAdapt
from typing import List, Generic, TypeVar, Type


AdapterType = TypeVar('AdapterType')


class AdapterRegistry(Generic[AdapterType]):
    def __init__(self):
        self.adapters: List[Type[Adapter]] = []

    def register(self, adapter: Type[Adapter]):
        self.adapters.append(adapter)

    def adapt(self, *args, **kwargs) -> AdapterType:
        for adapter in self.adapters:
            try:
                return adapter.adapt(*args, **kwargs)

            except UnableToAdapt:
                pass

        else:
            raise UnableToAdapt

