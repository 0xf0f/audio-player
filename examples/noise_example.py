from audio_player import AudioPlayer
from audio_player.audio_generator import noise

player = AudioPlayer()
player.set_source(noise.sox.WhiteNoiseGenerator())

player.settings.volume.set(.5)
player.play()
player.wait()
