from .lib.signals import SignalList


class Signals(SignalList):
    def __init__(self):
        super().__init__()
        self.stream_started = self.add_signal('stream_started')
        self.stream_stopped = self.add_signal('stream_stopped')
