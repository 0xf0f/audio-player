from . import qt
from audio_player import AudioPlayerProcessInterface


class QAudioPlayerProcessInterface(AudioPlayerProcessInterface):
    class QSignals(qt.QObject):
        source_changed = qt.pyqtSignal(object)
        state_changed = qt.pyqtSignal(str)
        duration_changed = qt.pyqtSignal(float)
        position_changed = qt.pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.qsignals = QAudioPlayerProcessInterface.QSignals()

        self.signals.source_changed.connect(self.qsignals.source_changed.emit)
        self.signals.state_changed.connect(self.qsignals.state_changed.emit)
        self.signals.position_changed.connect(self.qsignals.position_changed.emit)
        self.signals.duration_changed.connect(self.qsignals.duration_changed.emit)
