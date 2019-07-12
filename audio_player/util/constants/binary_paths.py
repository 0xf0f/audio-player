import sys
import struct
from pathlib import Path

cd: Path = Path(__file__).parent
binaries_folder: Path = cd.parents[1] / 'bin'

default_soundfont_path = str(binaries_folder/'timidity'/'sYnerGi-8Mb.sf2')

os_bits = struct.calcsize('P') * 8

if os_bits == 64:
    mrs_watson_binary_name = 'mrswatson64'
else:
    mrs_watson_binary_name = 'mrswatson'

if sys.platform.startswith('win32'):
    timidity_path = str(binaries_folder/'timidity'/'timidity.exe')
    openmpt123_path = str(binaries_folder/'openmpt123'/'openmpt123.exe')
    sox_path = str(binaries_folder/'sox'/'sox.exe')
    mrs_watson_path = str(binaries_folder/'mrswatson'/'Windows'/f'{mrs_watson_binary_name}.exe')

else:
    timidity_path = 'timidity'
    openmpt123_path = 'openmpt123'
    sox_path = 'sox'

    if sys.platform.startswith('darwin'):
        mrs_watson_path = str(binaries_folder/'mrswatson'/'Mac OS X'/mrs_watson_binary_name)
    else:
        mrs_watson_path = str(binaries_folder/'mrswatson'/'Linux'/mrs_watson_binary_name)
