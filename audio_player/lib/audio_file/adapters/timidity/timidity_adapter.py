import numpy as np
import threading as th
import mido

from cached_property import cached_property as cachedproperty
from .timidity_process import timidity_process
from audio_player.lib.audio_file.audio_file import AudioFile
from audio_player.lib.audio_info.audio_info import AudioInfo
from ... import UnableToOpenFileError


class TiMidityInfo(AudioInfo):
    def __init__(self, path):
        super().__init__(path)
        midi_object = mido.MidiFile(path)
        self.channels = 2
        self.sample_rate = 44100
        self.sample_count = int(midi_object.length * self.sample_rate)
        pass

    def channels(self) -> int:
        pass

    def sample_rate(self) -> int:
        pass

    def sample_count(self) -> int:
        pass


class TiMidityAdapter(AudioFile):
    info: AudioInfo

    def __init__(self, path, dtype=np.float32):
        super().__init__(path, dtype)
        try:
            self.process = timidity_process(path)
            self.info = TiMidityInfo(self.path)
            self.samples_read = 0
            self.read_lock = th.Lock()
            return
        except UnableToOpenFileError:
            pass

        raise UnableToOpenFileError(path)

    def __del__(self):
        self.close()

    @cachedproperty
    def info(self) -> AudioInfo:
        pass

    def read(self, n=-1, out: np.ndarray = None, int_buffer: np.ndarray=None) -> np.ndarray:
        # process = self.process
        with self.read_lock:
            if n == -1:
                n = self.info.sample_count

            if int_buffer is None:
                int_buffer = np.empty(
                    (n, self.info.channels), dtype='int16'
                )

            if out is None:
                out = np.empty(
                    (n, self.info.channels), dtype=self.dtype
                )

            bytes_read = self.process.stdout.readinto(int_buffer)
            samples_read = bytes_read//4
            np.divide(int_buffer, 32_768, out=out, casting='unsafe')

            self.samples_read += samples_read

            return out[:samples_read]

    def blocks(self, block_size=4096):
        int_buffer = np.empty(
            (block_size, self.info.channels), dtype='int16'
        )

        out_buffer = np.empty(
            (block_size, self.info.channels), dtype=self.dtype
        )

        while True:
            block = self.read(
                block_size, out=out_buffer, int_buffer=int_buffer
            )

            if block.size:
                yield block
            else:
                break

    def readable(self):
        return self.samples_read < self.info.sample_count

    def tell_time(self) -> float:
        # print(self.info.duration, self.samples_read, self.info.sample_count)
        return self.info.duration * (self.samples_read / self.info.sample_count)

    def seek_time(self, seconds: float) -> float:
        with self.read_lock:
            if self.process:
                self.process.terminate()
            self.process = timidity_process(self.path, start_time=seconds*1000)
            self.samples_read = int((seconds / self.info.duration) * self.info.sample_count)
            return seconds

    def close(self):
        if self.process:
            self.process.terminate()

    supported_extensions = (
        'mid',
        'mod',
        's3m'
        'xm',
    )
