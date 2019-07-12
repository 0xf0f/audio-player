import pymediainfo as mi
from ...base_object import AudioFileInfo
from audio_player.util.adapters import UnableToAdapt


class MediaInfoAdapter(AudioFileInfo):
    @classmethod
    def adapt(cls, path: str):
        try:
            result = cls(path)

            info: mi.MediaInfo = mi.MediaInfo.parse(path)
            for track in info.tracks:
                if track.track_type == 'Audio':
                    track_info = track.to_data()
                    result.channels = int(track_info['channel_s'])
                    result.sample_rate = int(track_info['sampling_rate'])
                    result.sample_count = int(track_info['samples_count'])

            return result

        except:
            raise UnableToAdapt

    def channels(self) -> int:
        pass

    def sample_rate(self) -> int:
        pass

    def sample_count(self) -> int:
        pass
