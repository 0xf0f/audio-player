from threading import Event

import tkinter as tk
from tkinter import filedialog

from audio_player import AudioPlayer

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

audio_player = AudioPlayer()
audio_player.settings.set_looping(True)
audio_player.play(file_path)

Event().wait()


