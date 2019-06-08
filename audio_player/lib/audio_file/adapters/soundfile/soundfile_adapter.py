import numpy as np
import soundfile as sf
from cached_property import cached_property as cachedproperty
from audio_player.lib.audio_file.audio_file import AudioFile
from audio_player.lib.audio_info.audio_info import AudioInfo
from ... import UnableToOpenFileError


class SoundFileAdapterInfo(AudioInfo):
    def __init__(self, path, file: sf.SoundFile):
        super().__init__(path)
        self.channels = file.channels
        self.sample_count = file.frames
        self.sample_rate = file.samplerate

    @cachedproperty
    def channels(self) -> int:
        pass

    @cachedproperty
    def sample_rate(self) -> int:
        pass

    @cachedproperty
    def sample_count(self) -> int:
        pass


class SoundFileAdapter(AudioFile):
    info: AudioInfo

    supported_extensions = (
        'wav',
        'flac',
    )

    def __init__(self, path, dtype=np.float32):
        super().__init__(path, dtype)

        try:
            self.file = sf.SoundFile(path)
            self.info = SoundFileAdapterInfo(path, self.file)
            return

        except:
            pass

        raise UnableToOpenFileError(path)

    @cachedproperty
    def info(self) -> AudioInfo:
        pass

    def read(self, n=-1, out: np.ndarray = None) -> np.ndarray:
        return self.file.read(n, dtype=self.dtype, out=out)

    def tell_time(self) -> float:
        return self.info.duration * (self.file.tell() / self.file.frames)

    def seek_time(self, seconds: float) -> float:
        return self.file.seek(
            int(seconds/self.info.duration * self.info.sample_count)
        )/self.info.sample_count*self.info.duration

    def readable(self):
        return self.file.tell() < self.file.frames

    def close(self):
        if self.file:
            self.file.close()
