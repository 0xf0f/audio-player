from audio_player.util.signals import SignalList


class Signals(SignalList):
    def __init__(self):
        super().__init__()

        self.source_changed = self.add_signal('source_changed')
        self.file_changed = self.add_signal('file_changed')
        self.state_changed = self.add_signal('state_changed')
        self.position_changed = self.add_signal('position_changed')
        self.duration_changed = self.add_signal('duration_changed')
