import subprocess as sp
from pathlib import Path
from audio_player.util.constants.binary_paths import (
    timidity_path as default_timidity_path,
    default_soundfont_path
)


def timidity_time_format(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f'{minutes}:{seconds}.{milliseconds}'


class ms(int):
    pass


def timidity_process(
        file_path,
        start_time: ms = 0,
        config=default_cfg_path,
        timidity_path=default_timidity_path,
):
    process = sp.Popen(
        [
            timidity_path,
            '-c', config,
            '-G', timidity_time_format(int(start_time)),
            '-Or1sl',
            '-o', '-',
            str(Path(file_path).absolute()),
        ],

        stdout=sp.PIPE,
        stderr=sp.DEVNULL,

        cwd=str(Path(config).parent),
    )
    return process
