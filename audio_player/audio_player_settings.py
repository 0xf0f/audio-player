from .audio_output_settings import Settings as AudioOutputSettings


class Settings(AudioOutputSettings):
    def __init__(self):
        super().__init__()
        self.looping = self.add_setting('looping', False)
