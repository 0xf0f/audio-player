from audio_player import AudioPlayer

player = AudioPlayer()
player.settings.soundfont.set('test_soundfont.sf2')

player.play('chopin.mid')
player.wait()
