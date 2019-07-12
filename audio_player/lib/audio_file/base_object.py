from abc import ABC, abstractmethod

from ..audio_source import AudioSource
from audio_player.util.file_adapter import FileAdapter


class AudioFile(FileAdapter, AudioSource, ABC):
    def __init__(self, path: str):
        FileAdapter.__init__(self, path)
        AudioSource.__init__(self)

    @classmethod
    @abstractmethod
    def adapt(cls, path: str):
        pass
