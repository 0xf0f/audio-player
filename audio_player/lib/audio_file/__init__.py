from audio_player.util.adapters import UnableToAdapt
from audio_player.util.exceptions import UnableToOpenFileError
from .adapters.registry import adapter_registry


def open(path):
    try:
        return adapter_registry.adapt(path)
    except UnableToAdapt:
        pass

    raise UnableToOpenFileError(path)
