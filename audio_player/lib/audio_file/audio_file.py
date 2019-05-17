from abc import ABC, abstractmethod
from cached_property import cached_property as cachedproperty
import numpy as np

from ..audio_info.audio_info import AudioInfo

adapter_types = []


class AudioFile(ABC):
    info: AudioInfo

    class UnableToOpenFileError(Exception):
        def __init__(self, path):
            super().__init__(f'Error occurred while opening {path}')

    @staticmethod
    def open(path, dtype=np.float32) -> 'AudioFile':
        for adapter_type in adapter_types:
            try:
                result = adapter_type(path, dtype)
                return result
            except AudioFile.UnableToOpenFileError:
                pass

        raise AudioFile.UnableToOpenFileError(path)

    @abstractmethod
    def __init__(self, path, dtype=np.float32):
        self.path = path
        self.dtype = dtype

    @abstractmethod
    @cachedproperty
    def info(self) -> AudioInfo:
        pass

    @cachedproperty
    def sample_width(self) -> int:
        return self.info.channels * np.dtype(self.dtype).itemsize

    @abstractmethod
    def read(self, n=-1, out: np.ndarray = None) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def readable(self):
        pass

    def blocks(self, block_size=4096):
        buffer = np.empty(
            (block_size, self.info.channels), dtype=self.dtype
        )

        while True:
            block = self.read(block_size, out=buffer)

            if block.size:
                yield block
            else:
                break

    # @abstractmethod
    # def read_bytes(self, n=-1) -> bytes:
    #     pass
    #
    # @abstractmethod
    # def byte_blocks(self, block_size=4096):
    #     pass

    @abstractmethod
    def tell_time(self) -> float:
        raise NotImplementedError

    # @abstractmethod
    # def seek(self, sample: int):
    #     raise NotImplementedError

    @abstractmethod
    def seek_time(self, seconds: float) -> float:
        raise NotImplementedError

    # @abstractmethod
    # def seek_timestamp(self, timestamp):
    #     raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError
