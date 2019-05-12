import samplerate as sr
import sounddevice as sd
import numpy as np

from .playback_settings import PlaybackSettings
from .block_processing import process_block

from .event_handling import EventEmitter


class AudioOutput(EventEmitter):
    def __init__(self, samplerate, channels, master_settings: PlaybackSettings):
        self.stream = sd.OutputStream(
            samplerate=samplerate, channels=channels,
            blocksize=4092, dtype='float32'
        )

        self.settings = PlaybackSettings()
        self.master_settings = master_settings

        self.resampler = sr.Resampler(channels=channels)

    def write(self, data: np.ndarray):
        volume = (
            self.settings.volume *
            self.master_settings.volume
        )

        pan = (
            self.master_settings.pan
        )

        balance = (
            self.settings.balance +
            self.master_settings.balance
        )

        data = process_block(data, volume, pan, balance)

        playback_rate = (
            self.settings.playback_rate *
            self.master_settings.playback_rate
        )

        data = self.resampler.process(data, playback_rate)

        try:
            self.stream.write(data)
            return len(data)

        except sd.PortAudioError:
            return 0

    def start(self):
        self.stream.start()
        self.event('stream_started')

    def stop(self):
        self.stream.stop()
        self.event('stream_stopped')
