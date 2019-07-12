import subprocess as sp
from pathlib import Path
from audio_player.util.constants.binary_paths import (
    timidity_path as default_timidity_path,
    default_soundfont_path
)


def timidity_time_format(milliseconds):
    milliseconds = int(milliseconds)
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f'{minutes}:{seconds}.{milliseconds}'


def timidity_decoding_process(
        file_path,
        from_position: float = 0,
        # config=default_cfg_path,
        soundfont=default_soundfont_path,
        timidity_path=default_timidity_path,
):
    soundfont = Path(soundfont)

    process = sp.Popen(
        [
            timidity_path,
            # '-c', config,
            '-x', f'soundfont "{soundfont.name}"',
            '-L', f'{soundfont.parent}',
            '-G', timidity_time_format(from_position * 1000),
            '-Or1sl',
            '-o', '-',
            f'{file_path}',
        ],

        stdout=sp.PIPE,
        stderr=sp.DEVNULL,

        # cwd=str(Path(config).parent),
    )
    return process
