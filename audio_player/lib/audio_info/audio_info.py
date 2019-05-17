from abc import abstractmethod, ABC
from cached_property import cached_property

adapter_types = []


class AudioInfo(ABC):
    class UnableToOpenFileError(Exception):
        def __init__(self, path):
            super().__init__(f'Error occurred while opening {path}')

    @staticmethod
    def open(path) -> 'AudioInfo':
        for adapter_type in adapter_types:
            try:
                return adapter_type(path)
            except AudioInfo.UnableToOpenFileError:
                pass

        raise AudioInfo.UnableToOpenFileError(path)

    @abstractmethod
    def __init__(self, path):
        self.path = path

    @abstractmethod
    @cached_property
    def channels(self) -> int:
        pass

    @abstractmethod
    @cached_property
    def sample_rate(self) -> int:
        pass

    @abstractmethod
    @cached_property
    def sample_count(self) -> int:
        pass

    @cached_property
    def duration(self) -> float:
        return self.sample_count / self.sample_rate
