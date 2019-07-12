import numpy as np
import soundfile as sf
from cached_property import cached_property

from audio_player.lib.audio_file.base_object import AudioFile
from audio_player.lib.audio_info.adapters.soundfile import SoundFileAdapter as SoundFileInfoAdapter
from audio_player.util.adapters import UnableToAdapt
from audio_player.util.constants.supported_extensions import soundfile_extensions


class SoundFileAdapter(AudioFile):
    supported_extensions = soundfile_extensions

    def __init__(self, path: str):
        super().__init__(path)

        self.file: sf.SoundFile = None

    @classmethod
    def adapt(cls, path: str):
        try:
            result = cls(path)
            result.file = sf.SoundFile(path)
            return result
        except:
            raise UnableToAdapt

    @cached_property
    def info(self) -> SoundFileInfoAdapter:
        result = SoundFileInfoAdapter(self.path)
        result.sample_rate = self.file.samplerate
        result.sample_count = self.file.frames
        result.channels = self.file.channels
        return result

    def read(self, n=-1, out: np.ndarray = None) -> np.ndarray:
        return self.file.read(n, dtype=np.float32, out=out)

    def tell_time(self) -> float:
        return self.info.duration * (self.file.tell() / self.file.frames)

    def seek_time(self, seconds: float) -> float:
        return self.file.seek(
            int(seconds/self.info.duration * self.info.sample_count)
        )/self.info.sample_count*self.info.duration

    # def readable(self):
    #     return self.file.tell() < self.file.frames

    def close(self):
        if self.file:
            self.file.close()
