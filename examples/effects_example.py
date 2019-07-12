from audio_player import AudioPlayer
from audio_player import audio_effect

player = AudioPlayer()
player.add_effects(
    audio_effect.Reverb(),
    audio_effect.Chorus(),
    audio_effect.Pitch(),
    audio_effect.Echo(),
)

player.play('test.wav')
player.wait()
