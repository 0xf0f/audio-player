from audio_player import AudioPlayer
from audio_player.lib import audio_pipeline

pipeline = audio_pipeline.Pipeline()

player = AudioPlayer()
player.set_pipeline(pipeline)

player.play()
player.wait()
