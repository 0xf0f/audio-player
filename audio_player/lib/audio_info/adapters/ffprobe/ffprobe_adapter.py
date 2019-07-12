from .ffprobe_process import probe
from ...base_object import AudioFileInfo
from audio_player.util.adapters import UnableToAdapt

from cached_property import cached_property as cachedproperty


class FFProbeAdapter(AudioFileInfo):
    @classmethod
    def adapt(cls, path: str):
        try:
            result = cls(path)
            probe_info = probe(path)

            for stream in probe_info['streams']:
                if stream['codec_type'] == 'audio':
                    # time_base = Fraction(stream['time_base'])
                    result.channels = int(stream['channels'])
                    result.duration = float(stream['duration'])
                    result.sample_rate = int(stream['sample_rate'])
                    result.sample_count = int(
                        result.duration * result.sample_rate
                    )
                    break

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

    @cachedproperty
    def duration(self) -> float:
        pass

