import subprocess as sp


def decode(
    path, from_position=0, sample_rate=None, channels=None
):
    format_options = []
    if sample_rate is not None:
        format_options.extend(('-ar', f'{sample_rate}'))
    if channels is not None:
        format_options.extend(('-ac', f'{channels}'))
    return sp.Popen(
        [
            'ffmpeg',
            '-ss', f'{from_position}',
            '-i', path,
            '-f', 'f32le',
            *format_options,
            '-'
        ],
        stdout=sp.PIPE,
        stderr=sp.DEVNULL
    )
