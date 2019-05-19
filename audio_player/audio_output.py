import samplerate as sr
import sounddevice as sd
import numpy as np

from .audio_processing import process_vpb

from .lib.settings import SettingList
from .lib.signals import SignalList


class AudioOutput:
    class Settings(SettingList):
        def __init__(self):
            super().__init__()

            self.volume = self.add_setting('volume', 1)
            self.pan = self.add_setting('pan', 0)
            self.playback_rate = self.add_setting('playback_rate', 1)
            self.balance = self.add_setting('balance', 0)

    class Signals(SignalList):
        def __init__(self):
            super().__init__()
            self.stream_started = self.add_signal('stream_started')
            self.stream_stopped = self.add_signal('stream_stopped')

    def __init__(self, samplerate, channels, master_settings: 'AudioOutput.Settings'):
        self.stream = sd.OutputStream(
            samplerate=samplerate, channels=channels,
            blocksize=0, dtype='float32'
        )

        self.signals = AudioOutput.Signals()
        self.settings = AudioOutput.Settings()

        self.master_settings = master_settings

        self.resampler = sr.Resampler(channels=channels)

    def write(self, data: np.ndarray):
        volume = (
            self.settings.volume.get() *
            self.master_settings.volume.get()
        )

        pan = (
            # self.settings.pan.get()
            self.master_settings.pan.get()
        )

        balance = (
            self.settings.balance.get() +
            self.master_settings.balance.get()
        )

        data = process_vpb(data, volume, pan, balance)

        playback_rate = (
            self.settings.playback_rate.get() *
            self.master_settings.playback_rate.get()
        )

        data = self.resampler.process(data, 1/playback_rate)

        try:
            self.stream.write(data)
            return len(data)

        except sd.PortAudioError:
            return 0

    def start(self):
        self.stream.start()
        self.signals.stream_started()

    def stop(self):
        self.stream.stop()
        self.signals.stream_stopped()
