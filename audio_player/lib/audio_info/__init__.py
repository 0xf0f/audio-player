from .audio_info import AudioInfo as _AudioInfo
from ..exceptions import UnableToOpenFileError

adapter_types = []

# Unfortunately mediainfo doesnt seem to return correct sample count values.
# This is disabled until a future time when this is solved.
# try:
#     from .adapters.mediainfo import MediaInfoAdapter as _MediaInfoAdapter
#     adapter_types.append(_MediaInfoAdapter)
# except ImportError:
#     _MediaInfoAdapter = None
#     pass

try:
    from .adapters.ffprobe import FFProbeAdapter as _FFProbeAdapter
    adapter_types.append(_FFProbeAdapter)
except ImportError:
    _FFProbeAdapter = None
    pass


def open(path) -> _AudioInfo:
    for adapter_type in adapter_types:
        try:
            return adapter_type(path)
        except UnableToOpenFileError:
            # print('nope', path, adapter_type)
            pass

    raise UnableToOpenFileError(path)
