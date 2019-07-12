from audio_player import audio_info

info = audio_info.open('loop.wav')

# you can get individual attributes
print(
    'duration', info.duration,
    'sample_count', info.sample_count,
    'sample_rate', info.sample_rate,
    'channels', info.channels,
)

# or all of them in a dict
print(info.as_dict())
