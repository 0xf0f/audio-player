from .playback_settings import PlaybackSettings


class AudioFilePlayerSettings(PlaybackSettings):
    def __init__(self):
        super().__init__()
        self.looping = False

    def set_looping(self, value):
        self.looping = value
        self.event('set_looping', value)
