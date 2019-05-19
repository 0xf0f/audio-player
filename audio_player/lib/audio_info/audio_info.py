from abc import abstractmethod, ABC
from cached_property import cached_property


class AudioInfo(ABC):
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
