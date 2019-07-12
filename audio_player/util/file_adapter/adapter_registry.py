# import re

from pathlib import Path
from typing import Union, Type, List

from .adapter import FileAdapter

from ..adapters import AdapterRegistry
from ..adapters import UnableToAdapt


# PathType = Union[str, Path]
# protocol_regex = re.compile(r'[a-zA-Z0-9]*://')
#
#
# def is_url(path):
#     return bool(protocol_regex.match(path))


class FileAdapterRegistry(AdapterRegistry):
    adapters: List[FileAdapter]

    def __init__(self):
        super().__init__()
        self.extension_mapping = dict()

    def register(self, adapter: Type[FileAdapter]):
        super().register(adapter)

        for extension in adapter.supported_extensions:
            try:
                mapping_list = self.extension_mapping[extension]
            except KeyError:
                mapping_list = []
                self.extension_mapping[extension] = mapping_list

            mapping_list.append(adapter)

    def adapt(self, path: str) -> FileAdapter:
        path_object = Path(path)

        if not path_object.exists():
            raise FileNotFoundError

        try:
            preferred_adapters = self.extension_mapping[path_object.suffix]
        except KeyError:
            return super().adapt(path)

        for adapter in preferred_adapters:
            try:
                return adapter.adapt(path)
            except UnableToAdapt:
                pass

        for adapter in self.adapters:
            if adapter not in preferred_adapters:
                try:
                    return adapter.adapt(path)
                except UnableToAdapt:
                    pass

        raise UnableToAdapt
