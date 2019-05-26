import numpy as np
from .audio_file import AudioFile as _AudioFile
from ..exceptions import UnableToOpenFileError

adapter_types = []

try:
    from .adapters.soundfile import SoundFileAdapter as _SoundFileAdapter
    adapter_types.append(_SoundFileAdapter)
except ImportError:
    _SoundFileAdapter = None
    pass

try:
    from .adapters.ffmpeg import FFMPEGAdapter as _FFMPEGAdapter
    adapter_types.append(_FFMPEGAdapter)
except ImportError as e:
    _FFMPEGAdapter = None
    pass

try:
    from .adapters.timidity import TiMidityAdapter as _TiMidityAdapter
    adapter_types.append(_TiMidityAdapter)
except ImportError as e:
    _TiMidityAdapter = None
    pass


def open(path, dtype=np.float32) -> _AudioFile:
    for adapter_type in adapter_types:
        print(adapter_type)
        try:
            return adapter_type(path, dtype)
        except UnableToOpenFileError:
            pass

    raise UnableToOpenFileError(path)
