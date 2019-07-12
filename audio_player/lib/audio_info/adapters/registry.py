from audio_player.util.file_adapter import FileAdapterRegistry
from ..base_object import AudioFileInfo


class AudioInfoAdapterRegistry(FileAdapterRegistry):
    def adapt(self, path: str) -> AudioFileInfo:
        return super().adapt(path)

    def register_adapters(self):
        from .soundfile import SoundFileAdapter
        from .ffprobe import FFProbeAdapter
        # from .mediainfo import MediaInfoAdapter
        from .mido import MidoAdapter
        # from .openmpt123 import OpenMPT123Adapter
        # from .sox import SoXAdapter

        self.register(SoundFileAdapter)
        self.register(FFProbeAdapter)
        # self.register(MediaInfoAdapter)
        self.register(MidoAdapter)
        # self.register(OpenMPT123Adapter)
        # self.register(SoXAdapter)


adapter_registry = AudioInfoAdapterRegistry()
adapter_registry.register_adapters()
