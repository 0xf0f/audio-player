from ..audio_info import AudioInfo
from ... import pymediainfo as mi
from cached_property import cached_property as cachedproperty


class MediaInfoAdapter(AudioInfo):
    def __init__(self, path):
        super().__init__(path)

        try:
            info: mi.MediaInfo = mi.MediaInfo.parse(path)
            for track in info.tracks:
                if track.track_type == 'Audio':
                    track_info = track.to_data()
                    self.channels = int(track_info['channel_s'])
                    self.sample_rate = int(track_info['sampling_rate'])
                    self.sample_count = int(track_info['samples_count'])
                    return

        except (RuntimeError, FileNotFoundError, IOError, KeyError):
            pass

        raise AudioInfo.UnableToOpenFileError(path)

    @cachedproperty
    def channels(self) -> int:
        pass

    @cachedproperty
    def sample_rate(self) -> int:
        pass

    @cachedproperty
    def sample_count(self) -> int:
        pass
