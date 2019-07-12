from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .audio_player import AudioPlayer
    from .audio_player_process_interface import AudioPlayerProcessInterface

__all__ = [
    'AudioPlayer',
    'AudioPlayerProcessInterface'
]


def play(path):
    from . import AudioPlayer
    player = AudioPlayer()
    player.play(path)
    player.wait()


def __getattr__(name):
    if name == 'AudioPlayer':
        from .audio_player import AudioPlayer
        return AudioPlayer

    elif name == 'AudioPlayerProcessInterface':
        from .audio_player_process_interface import AudioPlayerProcessInterface
        return AudioPlayerProcessInterface

    else:
        raise ImportError

