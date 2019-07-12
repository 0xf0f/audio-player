from abc import ABC, abstractmethod
from cached_property import cached_property as cachedproperty
import numpy as np

from ..audio_info.base_object import AudioInfo


class AudioSource(ABC):
    info: AudioInfo

    @abstractmethod
    @cachedproperty
    def info(self) -> AudioInfo:
        pass

    @cachedproperty
    def sample_width(self) -> int:
        return self.info.channels * np.dtype(np.float32).itemsize

    @abstractmethod
    def read(self, samples=-1, out: np.ndarray = None) -> np.ndarray:
        raise NotImplementedError

    # @abstractmethod
    # def readable(self):
    #     pass

    def blocks(self, block_size=4096):
        buffer = np.empty(
            (block_size, self.info.channels), dtype=np.float32
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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
