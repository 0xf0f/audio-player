from cached_property import cached_property

from audio_player.util.file_adapter import FileAdapter


class AudioInfo:
    """
    Objects of this class contain information about an audio info.
    """

    @cached_property
    def channels(self) -> int:
        """
        Cached property. Will be computed once then stored.

        :return: Number of channels in audio info.
        :type: int
        """
        raise NotImplementedError

    @cached_property
    def sample_rate(self) -> int:
        """
        Cached property. Will be computed once then stored.

        :return: Sample rate of audio info.
        :type: int
        """
        raise NotImplementedError

    @cached_property
    def sample_count(self) -> int:
        """
        Cached property. Will be computed once then stored.

        :return: Number of samples in audio info.
        :type: int
        """
        raise NotImplementedError

    @cached_property
    def duration(self) -> float:
        """
        Cached property. Will be computed once then stored.

        :return: Duration of audio in audio info, in seconds.
        :type: float
        """
        return self.sample_count / self.sample_rate

    def as_dict(self):
        """
        :return: All info attributes in one dict, with the keys:
            ('duration', 'sample_count', 'sample_rate', 'channels')
        :type: dict
        """
        return {
            'duration': self.duration,
            'sample_count': self.sample_count,
            'sample_rate': self.sample_rate,
            'channels': self.channels,
        }


class AudioFileInfo(FileAdapter, AudioInfo):
    def __init__(self, path: str):
        AudioInfo.__init__(self)
        FileAdapter.__init__(self, path)
