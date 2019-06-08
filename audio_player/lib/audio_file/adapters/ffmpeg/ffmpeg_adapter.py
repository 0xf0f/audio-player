import numpy as np
import threading as th

from cached_property import cached_property as cachedproperty
from .ffmpeg_process import decode
from audio_player.lib.audio_file.audio_file import AudioFile
from audio_player.lib.audio_info.audio_info import AudioInfo
from audio_player.lib import audio_info
from ... import UnableToOpenFileError


class FFMPEGAdapter(AudioFile):
    info: AudioInfo
    process = None

    def __init__(self, path, dtype=np.float32):
        super().__init__(path, dtype)
        try:
            self.process = decode(path)
            self.info = audio_info.open(self.path)
            self.samples_read = 0
            self.read_lock = th.Lock()
            return
        except:
            pass

        raise UnableToOpenFileError(path)

    def __del__(self):
        self.close()

    @cachedproperty
    def info(self) -> AudioInfo:
        pass

    def read(self, n=-1, out: np.ndarray = None) -> np.ndarray:
        # process = self.process
        with self.read_lock:
            if n == -1:
                n = self.info.sample_count

            if out is None:
                out = np.empty(
                    (n, self.info.channels), dtype=self.dtype
                )

            bytes_read = self.process.stdout.readinto(out)
            samples_read = bytes_read//self.sample_width

            self.samples_read += samples_read

            return out[:samples_read]

    def readable(self):
        return self.samples_read < self.info.sample_count

    def tell_time(self) -> float:
        # print(self.info.duration, self.samples_read, self.info.sample_count)
        return self.info.duration * (self.samples_read / self.info.sample_count)

    def seek_time(self, seconds: float) -> float:
        with self.read_lock:
            if self.process:
                self.process.terminate()
            self.process = decode(self.path, from_position=seconds)
            self.samples_read = int((seconds / self.info.duration) * self.info.sample_count)
            return seconds

    def close(self):
        if self.process:
            self.process.terminate()
