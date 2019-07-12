import tkinter as tk
from tkinter import filedialog
from audio_player import AudioPlayer


def get_file_path():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    return file_path


player = AudioPlayer()
player.settings.looping.set(True)
player.play(get_file_path())
player.wait()
