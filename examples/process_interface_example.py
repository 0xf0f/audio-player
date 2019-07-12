from audio_player import AudioPlayerProcessInterface

if __name__ == '__main__':
    player = AudioPlayerProcessInterface()
    player.start_process()

    # player.settings.looping.set(True)
    player.play('loop.wav')
    player.wait()
