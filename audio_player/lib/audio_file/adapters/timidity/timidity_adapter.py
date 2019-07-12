import numpy as np
import subprocess as sp
import threading as th

from .timidity_process import timidity_decoding_process
from cached_property import cached_property

from ...base_object import AudioFile
from ....audio_info.adapters.mido import MidoAdapter
from audio_player.util.adapters import UnableToAdapt


class TiMidityAdapter(AudioFile):
    info: MidoAdapter
    process = None

    def __init__(self, path: str):
        super().__init__(path)

        self.process: sp.Popen = None
        self.samples_read = 0
        self.read_lock = th.Lock()

    @classmethod
    def adapt(cls, path: str):
        try:
            result = cls(path)
            result.info = MidoAdapter.adapt(path)
            result.process = timidity_decoding_process(path)
            return result
        except:
            raise UnableToAdapt

    @cached_property
    def info(self) -> MidoAdapter:
        pass

    def read(self, n=-1, out: np.ndarray = None, int_buffer: np.ndarray=None) -> np.ndarray:
        with self.read_lock:
            if n == -1:
                n = self.info.sample_count

            if int_buffer is None:
                int_buffer = np.empty(
                    (n, self.info.channels), dtype='int16'
                )

            if out is None:
                out = np.empty(
                    (n, self.info.channels), dtype=np.float32
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
            (block_size, self.info.channels), dtype=np.float32
        )

        while True:
            block = self.read(
                block_size, out=out_buffer, int_buffer=int_buffer
            )

            if block.size:
                yield block
            else:
                break

    def tell_time(self) -> float:
        return self.info.duration * (self.samples_read / self.info.sample_count)

    def seek_time(self, seconds: float) -> float:
        with self.read_lock:
            if self.process:
                self.process.terminate()
            self.process = timidity_decoding_process(self.path, from_position=seconds)
            self.samples_read = int((seconds / self.info.duration) * self.info.sample_count)
            return seconds

    # def readable(self):
    #     return self.file.tell() < self.file.frames

    def close(self):
        if self.process:
            self.process.terminate()
