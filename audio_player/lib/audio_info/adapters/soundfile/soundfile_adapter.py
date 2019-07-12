import soundfile as sf
from ...base_object import AudioFileInfo
from audio_player.util.adapters import UnableToAdapt
from audio_player.util.constants.supported_extensions import soundfile_extensions

from cached_property import cached_property as cachedproperty


class SoundFileAdapter(AudioFileInfo):
    supported_extensions = soundfile_extensions

    @classmethod
    def adapt(cls, path: str):
        try:
            with sf.SoundFile(path) as file:
                result = cls(path)
                result.channels = file.channels
                result.sample_rate = file.samplerate
                result.sample_count = file.frames
                return result

        except:
            raise UnableToAdapt

    @cachedproperty
    def channels(self) -> int:
        pass

    @cachedproperty
    def sample_rate(self) -> int:
        pass

    @cachedproperty
    def sample_count(self) -> int:
        pass
