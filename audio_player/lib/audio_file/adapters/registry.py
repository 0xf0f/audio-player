from audio_player.util.file_adapter import FileAdapterRegistry
from ..base_object import AudioFile


class AudioFileAdapterRegistry(FileAdapterRegistry):
    def __init__(self):
        super().__init__()

        from .soundfile import SoundFileAdapter
        from .ffmpeg import FFMPEGAdapter
        from .timidity import TiMidityAdapter
        # from .openmpt123 import OpenMPT123Adapter

        self.register(SoundFileAdapter)
        self.register(FFMPEGAdapter)
        self.register(TiMidityAdapter)
        # self.register(OpenMPT123Adapter)

    def adapt(self, path) -> AudioFile:
        return super().adapt(path)


adapter_registry = AudioFileAdapterRegistry()

