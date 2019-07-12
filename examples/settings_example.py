from audio_player import AudioPlayer

player = AudioPlayer()

player.settings.volume.set(0.5)
player.settings.pan.set(-1.0)
player.settings.balance.set(0.5)
player.settings.playback_rate.set(0.2)

player.settings.looping.set(True)
