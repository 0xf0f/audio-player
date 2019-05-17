from . import audio_info as _audio_info
open = _audio_info.AudioInfo.open

# Unfortunately mediainfo doesnt seem to return correct sample count values.
# This is disabled until a future time when this is solved.
# try:
#     from .adapters.mediainfo_adapter import MediaInfoAdapter as _MediaInfoAdapter
#     _audio_info.adapter_types.append(_MediaInfoAdapter)
# except ImportError:
#     _MediaInfoAdapter = None
#     pass

try:
    from .adapters.ffprobe_adapter import FFProbeAdapter as _FFProbeAdapter
    _audio_info.adapter_types.append(_FFProbeAdapter)
except ImportError:
    _FFProbeAdapter = None
    pass
