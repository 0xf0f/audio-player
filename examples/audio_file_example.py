from audio_player import audio_file

with audio_file.open('loop.wav') as file:
    for block in file.blocks():
        print(block)
