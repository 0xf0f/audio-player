import samplerate as sr
import sounddevice as sd
import numpy as np

from .audio_processing import process_vpb
from .audio_output_signals import Signals as AudioOutputSignals
from .audio_output_settings import Settings as AudioOutputSettings


class AudioOutput:
    def __init__(self, samplerate, channels, master_settings: AudioOutputSettings):
        self.stream = sd.OutputStream(
            samplerate=samplerate, channels=channels,
            blocksize=0, dtype='float32'
        )

        self.signals = AudioOutputSignals()
        self.settings = AudioOutputSettings()

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
