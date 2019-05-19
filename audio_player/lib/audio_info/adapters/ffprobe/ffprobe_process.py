import subprocess as sp
import json


def probe(path):
    process = sp.Popen(
        [
            'ffprobe', path,
            '-print_format', 'json=c=1',
            '-show_streams', '-show_format',
            '-loglevel', 'quiet'
        ],

        stdout=sp.PIPE, stderr=sp.DEVNULL,
    )

    return json.load(process.stdout)
