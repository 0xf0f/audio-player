import sys
from pathlib import Path

cd: Path = Path(__file__).parent
sys.path.append(str(cd))
sys.path.append(str(cd.parent))

import multiprocessing as mp
from audio_player import AudioPlayerProcess
from types import MethodType
from examples import qt

# This test requires PyQt5 to work.

# class Test:
# 	a = 1
# 	b = 2
# 	c = 3
#
# Test.__dict__


# class Test:
#     for i in range(10):
#         print(i)

def format_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    result = f'{minutes:02}:{seconds:02}.{milliseconds:03}'
    if hours:
        result = f'{hours:02}:{result}'

    return result


class QAudioPlayerProcess(AudioPlayerProcess):
    class Signals(qt.QObject):
        file_changed = qt.pyqtSignal(str)
        state_changed = qt.pyqtSignal(str)
        duration_changed = qt.pyqtSignal(float, int, int)
        position_changed = qt.pyqtSignal(float)

    class SignalThread(qt.QThread):
        def __init__(
            self,
            signal_queue: mp.Queue,
            signals: 'QAudioPlayerProcess.Signals'
        ):
            super().__init__()
            self.event_queue = signal_queue
            self.signals = signals

        def run(self):
            while True:
                name, args, kwargs = self.event_queue.get()
                if name == 'position_changed':
                    self.signals.position_changed.emit(args[0])

                elif name == 'duration_changed':
                    self.signals.duration_changed.emit(
                        kwargs['seconds'], kwargs['bytes'], kwargs['samples']
                    )

                elif name == 'state_changed':
                    self.signals.state_changed.emit(args[0])

    def __init__(self):
        super().__init__()
        self.event_queue = mp.Queue()

    def process_init(self):
        super().process_init()

        from audio_player.event_handling import Event

        def queue_event(source: Event, *args, **kwargs):
            self.event_queue.put_nowait((source.name, args, kwargs))

        for event in self.audio_player.events:
            event.emit = MethodType(queue_event, event)

    def get_signal_thread(self):
        signals = QAudioPlayerProcess.Signals()
        signal_thread = QAudioPlayerProcess.SignalThread(
            self.event_queue, signals
        )
        return signals, signal_thread


class AudioPlayerWindow(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.player_process = QAudioPlayerProcess()

        self.drop_label = qt.QLabel('Drop files here to play.')
        self.drop_label.setAlignment(qt.Constants.AlignCenter)
        self.drop_label.setFixedHeight(128)
        self.drop_label.setMinimumWidth(256)

        self.play_button = qt.QPushButton('Play')
        self.play_button.clicked.connect(
            lambda: self.player_process.send_command(
                'toggle'
            )
        )

        self.replay_button = qt.QPushButton('Replay')
        self.replay_button.clicked.connect(
            lambda: (
                self.player_process.send_command('rewind'),
                self.player_process.send_command('resume'),
            )
        )

        self.stop_button = qt.QPushButton('Stop')
        self.stop_button.clicked.connect(
            lambda: (
                self.player_process.send_command('stop'),
            )
        )

        self.loop_button = qt.QPushButton('Looping')
        self.loop_button.setCheckable(True)
        self.loop_button.toggled.connect(
            lambda toggled: self.player_process.send_command(
                'set_looping', toggled
            )
        )

        self.volume_slider = qt.QSlider()
        self.volume_slider.setOrientation(qt.Constants.Vertical)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.setToolTip('Volume')
        self.volume_slider.valueChanged.connect(
            lambda value: self.player_process.send_command(
                'set_volume', value/100
            )
        )

        self.pan_slider = qt.QSlider()
        self.pan_slider.setOrientation(qt.Constants.Vertical)
        self.pan_slider.setMaximum(100)
        self.pan_slider.setMinimum(-100)
        self.pan_slider.setValue(0)
        self.pan_slider.setToolTip('Pan')
        self.pan_slider.valueChanged.connect(
            lambda value: self.player_process.send_command(
                'set_pan', value/100
            )
        )

        self.playback_rate_slider = qt.QSlider()
        self.playback_rate_slider.setOrientation(qt.Constants.Vertical)
        self.playback_rate_slider.setMaximum(200)
        self.playback_rate_slider.setMinimum(50)
        self.playback_rate_slider.setValue(100)
        self.playback_rate_slider.setToolTip('Playback Rate')
        self.playback_rate_slider.valueChanged.connect(
            lambda value: self.player_process.send_command(
                'set_playback_rate', value/100
            )
        )

        position_label_font = qt.QFont()
        position_label_font.setPointSize(16)

        self.position = 0
        self.duration = 0
        self.position_label = qt.QLabel()
        self.position_label.setFont(position_label_font)
        self.position_label.setAlignment(qt.Constants.AlignCenter)

        def update_position_label():
            self.position_label.setText(
                f'{format_time(int(self.position*self.duration))}/'
                f'{format_time(self.duration)}'
            )

        update_position_label()

        self.vboxwidget = qt.QWidget()
        self.vboxlayout = qt.QVBoxLayout(self.vboxwidget)
        self.vboxlayout.addWidget(self.drop_label)
        self.vboxlayout.addStretch()
        self.vboxlayout.addWidget(self.position_label)
        self.vboxlayout.addWidget(self.play_button)
        self.vboxlayout.addWidget(self.replay_button)
        self.vboxlayout.addWidget(self.stop_button)
        self.vboxlayout.addWidget(self.loop_button)

        self.hboxlayout = qt.QHBoxLayout(self)
        self.hboxlayout.addWidget(self.playback_rate_slider)
        self.hboxlayout.addWidget(self.pan_slider)
        self.hboxlayout.addWidget(self.volume_slider)
        self.hboxlayout.addWidget(self.vboxwidget)

        (
            self.player_process_signals,
            self.player_process_signal_thread
        ) = self.player_process.get_signal_thread()

        def on_duration_changed(duration):
            self.duration = int(duration*1000)
            update_position_label()

        def on_position_changed(position):
            self.position = position
            update_position_label()

        def on_state_changed(state):
            if state == 'playing':
                self.play_button.setText('Pause')
            else:
                self.play_button.setText('Play')

        self.player_process_signals.duration_changed.connect(
            on_duration_changed
        )

        self.player_process_signals.position_changed.connect(
            on_position_changed
        )

        self.player_process_signals.state_changed.connect(
            on_state_changed
        )

        self.setWindowTitle('Audio Player')
        self.setAcceptDrops(True)
        self.player_process_signal_thread.start()
        self.player_process.start()

    def dragEnterEvent(self, event: qt.QDragEnterEvent):
        mime_data: qt.QMimeData = event.mimeData()
        if mime_data.hasUrls():
            event.accept()

    def dropEvent(self, event: qt.QDropEvent):
        mime_data: qt.QMimeData = event.mimeData()
        if mime_data.hasUrls():
            url: qt.QUrl = mime_data.urls()[0]
            path = url.toLocalFile()
            self.player_process.send_command(
                'play', path
            )


if __name__ == '__main__':
    def main():
        import sys
        app = qt.QApplication(sys.argv)
        sys.excepthook = sys.__excepthook__

        audio_player_window = AudioPlayerWindow()
        audio_player_window.show()

        app.exec()

    main()
