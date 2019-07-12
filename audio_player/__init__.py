from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .lib.audio_player.base_object import AudioPlayer
    from .lib.audio_player_process.audio_player_process_interface import AudioPlayerProcessInterface

    from .lib import audio_file
    from .lib import audio_info
    from .lib import audio_processor


__all__ = [
    'AudioPlayer',
    'AudioPlayerProcessInterface',
    'audio_file',
    'audio_info',
    'audio_processor',
    'play'
]


def play(path):
    from . import AudioPlayer
    player = AudioPlayer()
    player.play(path)
    player.wait()


def __getattr__(name):
    if name == 'AudioPlayer':
        from .lib.audio_player.base_object import AudioPlayer
        return AudioPlayer

    elif name == 'AudioPlayerProcessInterface':
        from .lib.audio_player_process.audio_player_process_interface import AudioPlayerProcessInterface
        return AudioPlayerProcessInterface

    elif name == 'audio_file':
        from .lib import audio_file
        return audio_file

    elif name == 'audio_info':
        from .lib import audio_info
        return audio_info

    elif name == 'audio_processor':
        from .lib import audio_processor

    elif name == 'play':
        return play

    else:
        raise ImportError

