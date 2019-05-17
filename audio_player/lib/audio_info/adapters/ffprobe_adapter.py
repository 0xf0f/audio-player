from ..audio_info import AudioInfo
from .ffprobe_process import probe
from cached_property import cached_property as cachedproperty


class FFProbeAdapter(AudioInfo):
    def __init__(self, path):
        super().__init__(path)

        try:
            probe_info = probe(path)
            for stream in probe_info['streams']:
                if stream['codec_type'] == 'audio':
                    # time_base = Fraction(stream['time_base'])
                    self.channels = int(stream['channels'])
                    self.duration = float(stream['duration'])
                    self.sample_rate = int(stream['sample_rate'])
                    self.sample_count = int(self.duration * self.sample_rate)
                    return

        except KeyError:
            pass

        raise AudioInfo.UnableToOpenFileError(path)

    @cachedproperty
    def duration(self) -> float:
        pass

    @cachedproperty
    def channels(self) -> int:
        pass

    @cachedproperty
    def sample_rate(self) -> int:
        pass

    @cachedproperty
    def sample_count(self) -> int:
        pass
