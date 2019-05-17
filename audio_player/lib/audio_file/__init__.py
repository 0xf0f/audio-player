from . import audio_file as _audio_file
open = _audio_file.AudioFile.open
UnableToOpenFileError = _audio_file.AudioFile.UnableToOpenFileError

try:
    from .adapters.soundfile_adapter import SoundFileAdapter as _SoundFileAdapter
    _audio_file.adapter_types.append(_SoundFileAdapter)
except ImportError:
    _SoundFileAdapter = None
    pass

try:
    from .adapters.ffmpeg_adapter import FFMPEGAdapter as _FFMPEGAdapter
    _audio_file.adapter_types.append(_FFMPEGAdapter)
except ImportError as e:
    _FFMPEGAdapter = None
    pass
