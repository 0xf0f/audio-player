from audio_player import AudioPlayer

player = AudioPlayer()
player.signals.position_changed.connect(
    lambda position: print('position:', position)
)

player.signals.file_changed.connect(
    lambda file: print('file:', file)
)

player.signals.source_changed.connect(
    lambda source: print('info:', source)
)

player.signals.duration_changed.connect(
    lambda duration: print('duration:', duration)
)

player.signals.state_changed.connect(
    lambda state: print('state:', state)
)

player.play('loop.wav')
player.wait()
