from abc import ABC, abstractmethod
from ..audio_block import AudioBlock


class AudioSink(ABC):
    @abstractmethod
    def write(self, block: AudioBlock):
        pass

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
