### Introduction
TODO

### Installation
`pip install git+http://github.com/0xf0f/audio-player`
https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg

timidity

sox

### Examples
```python
# Basic playback

from audio_player import AudioPlayer

player = AudioPlayer()
player.play('file.wav')
```

```python
from audio_player import AudioPlayer

player = AudioPlayer()
player.set_file('file.wav')
new_position = player.file.info.duration / 2
player.seek_time(new_position)
player.resume()

```
### Documentation
TODO

### Credits
- soundfile
- sounddevice
- samplerate
- numba
- numpy
- cached_property

- timidity
- ffmpeg
- loop.wav/loop2.wav
- sox
- pyqt5