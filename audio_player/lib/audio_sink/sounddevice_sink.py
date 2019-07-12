import sounddevice as sd

from audio_player.lib.audio_block import AudioBlock
from .base_object import AudioSink
from typing import Tuple, Dict


class SoundDeviceSink(AudioSink):
    def __init__(self, device=None):
        super().__init__()
        self.streams: Dict[Tuple[int, int], sd.OutputStream] = dict()
        self.device = device

    def get_stream(self, sample_rate, channels):
        try:
            return self.streams[sample_rate, channels]
        except KeyError:
            stream = sd.OutputStream(
                device=self.device,
                samplerate=sample_rate,
                channels=channels,
                dtype='float32'
            )
            stream.start()
            self.streams[sample_rate, channels] = stream
            return stream

    def write(self, block: AudioBlock):
        self.get_stream(
            block.info.sample_rate,
            block.info.channels
        ).write(block.data)

    def open(self):
        for stream in self.streams.values():
            stream.start()

    def close(self):
        for stream in self.streams.values():
            stream.close()
