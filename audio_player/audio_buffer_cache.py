from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .audio_buffer import AudioBuffer


class ExceedsCacheSize(Exception):
    pass


class AudioBufferCache:
    def __init__(self, max_size=128*1024*1024):
        self.max_size = max_size
        self.items: Dict[Any, 'AudioBuffer'] = dict()
        self.combined_length = 0

    def put(self, name, buffer: 'AudioBuffer'):
        if len(buffer) > self.max_size:
            raise ExceedsCacheSize

        else:
            keys = iter(self.items.keys())
            while (self.max_size - self.combined_length) < len(buffer):
                self.get(next(keys))
            self.items[name] = buffer
            self.combined_length += len(buffer)

    def get(self, name):
        item = self.items.pop(name)
        self.combined_length -= len(item)
        return item
