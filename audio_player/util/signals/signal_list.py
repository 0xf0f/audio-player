from .signal import Signal
from typing import Any, Dict


class SignalList:
    def __init__(self):
        self.signals: Dict[str, Signal] = {}

    def add_signal(self, name):
        signal = Signal(name)
        self.signals[name] = signal

        return signal

    def __getitem__(self, item):
        return self.signals[item]

    def __iter__(self):
        yield from self.signals.values()
