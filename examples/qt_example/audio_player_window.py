from examples.qt_example import qt
from examples.qt_example.q_audio_player_process_interface import QAudioPlayerProcessInterface
from examples.qt_example.format_time import format_time
from examples.qt_example.waveform_slider import WaveformSlider


class AudioPlayerWindow(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.controller = QAudioPlayerProcessInterface()

        self.drop_label = qt.QLabel('Drop files here to play.')
        self.drop_label.setAlignment(qt.Constants.AlignCenter)
        self.drop_label.setFixedHeight(128)
        self.drop_label.setMinimumWidth(256)

        self.play_button = qt.QPushButton('Play')
        self.replay_button = qt.QPushButton('Replay')

        self.play_button.clicked.connect(self.controller.toggle)
        self.replay_button.clicked.connect(
            lambda: (self.controller.rewind(), self.controller.resume())
        )

        self.stop_button = qt.QPushButton('Stop')
        self.stop_button.clicked.connect(self.controller.stop)

        self.loop_button = qt.QPushButton('Looping')
        self.loop_button.setCheckable(True)
        self.loop_button.toggled.connect(self.controller.settings.looping.set)

        self.volume_slider = qt.QSlider()
        self.volume_slider.setOrientation(qt.Constants.Vertical)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.setToolTip('Volume')
        self.volume_slider.valueChanged.connect(
            lambda value: self.controller.settings.volume.set(value/100)
        )

        self.pan_slider = qt.QSlider()
        self.pan_slider.setOrientation(qt.Constants.Vertical)
        self.pan_slider.setMaximum(100)
        self.pan_slider.setMinimum(-100)
        self.pan_slider.setValue(0)
        self.pan_slider.setToolTip('Pan')
        self.pan_slider.valueChanged.connect(
            lambda value: self.controller.settings.pan.set(value/100)
        )

        self.playback_rate_slider = qt.QSlider()
        self.playback_rate_slider.setOrientation(qt.Constants.Vertical)
        self.playback_rate_slider.setMaximum(200)
        self.playback_rate_slider.setMinimum(50)
        self.playback_rate_slider.setValue(100)
        self.playback_rate_slider.setToolTip('Playback Rate')
        self.playback_rate_slider.valueChanged.connect(
            lambda value: self.controller.settings.playback_rate.set(value/100)
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
                f'{format_time(self.position)}/'
                f'{format_time(self.duration)}'
            )

        update_position_label()

        self.seek_bar: qt.QSlider = WaveformSlider()
        self.seek_bar.setOrientation(qt.Constants.Horizontal)
        self.seek_bar.setMinimum(0)
        self.seek_bar.setMaximum(100)
        self.seek_bar.position_updated.connect(
            lambda position: self.controller.seek_time(position/1000)
        )

        self.vboxwidget = qt.QWidget()
        self.vboxlayout = qt.QVBoxLayout(self.vboxwidget)
        self.vboxlayout.addWidget(self.drop_label)
        self.vboxlayout.addStretch()
        self.vboxlayout.addWidget(self.position_label)
        self.vboxlayout.addWidget(self.seek_bar)
        self.vboxlayout.addWidget(self.play_button)
        self.vboxlayout.addWidget(self.replay_button)
        self.vboxlayout.addWidget(self.stop_button)
        self.vboxlayout.addWidget(self.loop_button)

        self.hboxlayout = qt.QHBoxLayout(self)
        self.hboxlayout.addWidget(self.playback_rate_slider)
        self.hboxlayout.addWidget(self.pan_slider)
        self.hboxlayout.addWidget(self.volume_slider)
        self.hboxlayout.addWidget(self.vboxwidget)

        def on_duration_changed(duration):
            self.duration = int(duration*1000)
            self.seek_bar.setMaximum(self.duration)
            update_position_label()

        def on_position_changed(position):
            self.position = int(position*1000)
            if not self.seek_bar.mouse_down:
                self.seek_bar.setSliderPosition(
                    position*1000
                )

            update_position_label()

        def on_state_changed(state):
            if state == 'playing':
                self.play_button.setText('Pause')
            else:
                self.play_button.setText('Play')

        self.controller.qsignals.duration_changed.connect(
            on_duration_changed
        )

        self.controller.qsignals.position_changed.connect(
            on_position_changed
        )

        self.controller.qsignals.state_changed.connect(
            on_state_changed
        )

        self.controller.qsignals.file_changed.connect(
            self.seek_bar.set_path
        )

        self.setWindowTitle('Audio Player')
        self.setAcceptDrops(True)

        self.controller.start_process()

    def dragEnterEvent(self, event: qt.QDragEnterEvent):
        mime_data: qt.QMimeData = event.mimeData()
        if mime_data.hasUrls():
            event.accept()

    def dropEvent(self, event: qt.QDropEvent):
        mime_data: qt.QMimeData = event.mimeData()
        if mime_data.hasUrls():
            url: qt.QUrl = mime_data.urls()[0]
            path = url.toLocalFile()
            self.controller.play(path)

    def __del__(self):
        if self.controller and self.controller.process:
            self.controller.process.kill()
