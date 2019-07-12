import mido
from ...base_object import AudioFileInfo
from audio_player.util.adapters import UnableToAdapt

from cached_property import cached_property as cachedproperty


class MidoAdapter(AudioFileInfo):
    supported_extensions = (
        '.mid',
    )

    channels = 2
    sample_rate = 44100

    @classmethod
    def adapt(cls, path: str):
        try:
            with mido.MidiFile(path) as file:
                result = cls(path)
                result.duration = file.length
                result.sample_count = int(result.duration*result.sample_rate)
                return result

        except:
            raise UnableToAdapt

    @cachedproperty
    def sample_count(self) -> int:
        pass

    @cachedproperty
    def duration(self) -> float:
        pass
