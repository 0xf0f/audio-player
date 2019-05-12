from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .audio_output import AudioOutput


class AudioOutputCache:
    def __init__(self, max_length=8):
        self.outputs: Dict[Any, 'AudioOutput'] = dict()
        self.max_length = max_length

    def __setitem__(self, name, output):
        keys = iter(self.outputs.keys())
        while len(self.outputs) >= self.max_length:
            output = self.outputs.pop(next(keys))
            output.stream.close()
        self.outputs[name] = output

    def __getitem__(self, name):
        return self.outputs[name]