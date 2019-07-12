import numpy as np
import subprocess as sp
import threading as th

from .ffmpeg_process import ffmpeg_decoding_process
from cached_property import cached_property

from ...base_object import AudioFile
from audio_player.lib.audio_info.adapters.ffprobe import FFProbeAdapter
from audio_player.util.adapters import UnableToAdapt


class FFMPEGAdapter(AudioFile):
    info: FFProbeAdapter
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
            result.info: FFProbeAdapter = FFProbeAdapter.adapt(path)
            result.process = ffmpeg_decoding_process(path)
            # print('yo')
            return result
        except:
            # print('crap')
            raise UnableToAdapt

    @cached_property
    def info(self) -> FFProbeAdapter:
        pass

    def read(self, n=-1, out: np.ndarray = None) -> np.ndarray:
        with self.read_lock:
            if n == -1:
                n = self.info.sample_count

            if out is None:
                out = np.empty(
                    (n, self.info.channels), dtype=np.float32
                )

            bytes_read = self.process.stdout.readinto(out)
            samples_read = bytes_read//self.sample_width

            self.samples_read += samples_read

            return out[:samples_read]

    def tell_time(self) -> float:
        return self.info.duration * (self.samples_read / self.info.sample_count)

    def seek_time(self, seconds: float) -> float:
        with self.read_lock:
            if self.process:
                self.process.terminate()
            self.process = ffmpeg_decoding_process(self.path, from_position=seconds)
            self.samples_read = int((seconds / self.info.duration) * self.info.sample_count)
            return seconds

    # def readable(self):
    #     return self.file.tell() < self.file.frames

    def close(self):
        if self.process:
            self.process.terminate()
