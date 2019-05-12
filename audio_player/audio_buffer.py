import io
import numpy as np
import audioread as ar

from .event_handling import Event


class AudioBuffer:
    class Events:
        def __init__(self, source: 'AudioBuffer'):
            self.file_exhausted = Event('file_exhausted', source)

    def __init__(self, path):
        self.path = path

        self.file = ar.audio_open(path)
        self.file_iterator = iter(self.file)
        self.file_exhausted = False

        self.bytes_per_sample = self.file.channels * 2
        self.bytes_per_second = self.file.samplerate * self.bytes_per_sample

        self.total_bytes = int(self.file.duration * self.bytes_per_second)
        self.total_samples = self.total_bytes // self.bytes_per_sample

        self.buffer = io.BytesIO()
        self.buffer_length = 0

        self.events = AudioBuffer.Events(self)

        # self.preread_seconds(0.05)

    def seek(self, n):
        self.buffer.seek(n)

    def read(self, n, numpy_array=False):
        current = self.buffer.tell()

        while not self.file_exhausted and self.buffer_length - current < n:
            self.buffer.seek(0, io.SEEK_END)
            try:
                chunk = next(self.file_iterator)
                self.buffer.write(chunk)
                self.buffer_length += len(chunk)

            except StopIteration:
                self.file_exhausted = True
                self.file.close()
                self.events.file_exhausted()

        self.buffer.seek(current)

        if numpy_array:
            array: np.ndarray = np.frombuffer(
                self.buffer.read(n), dtype='int16',
            )

            array.shape = (
                array.shape[0]//self.file.channels, self.file.channels
            )

            array = array.astype('float32')
            array /= 32_767

            return array

        else:
            return self.buffer.read(n)

    def preread(self, n):
        current = self.tell()
        self.buffer.seek(0, io.SEEK_END)
        self.read(n)
        self.buffer.seek(current)

    def preread_seconds(self, n):
        self.preread(int(n * self.bytes_per_second))

    def tell(self):
        return self.buffer.tell()

    def __len__(self):
        return self.buffer_length

    def __bool__(self):
        return True
