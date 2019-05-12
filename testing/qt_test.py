from testing import qt
from audio_player import AudioPlayerProcess

# This test requires PyQt5 to work.


class TestWindow(qt.QWidget):
    def __init__(self):
        super().__init__()

        self.player_process = AudioPlayerProcess()
        self.player_process.start()

        self.drop_label = qt.QLabel('Drop files here to play.')
        self.drop_label.setAlignment(qt.Constants.AlignCenter)
        self.drop_label.setFixedHeight(128)
        self.drop_label.setMinimumWidth(256)

        self.play_button = qt.QPushButton('Play')
        self.play_button.clicked.connect(
            lambda: self.player_process.send_command(
                'toggle_playing'
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

        self.vboxwidget = qt.QWidget()
        self.vboxlayout = qt.QVBoxLayout(self.vboxwidget)
        self.vboxlayout.addWidget(self.drop_label)
        self.vboxlayout.addStretch()
        self.vboxlayout.addWidget(self.play_button)
        self.vboxlayout.addWidget(self.replay_button)
        self.vboxlayout.addWidget(self.stop_button)
        self.vboxlayout.addWidget(self.loop_button)

        self.hboxlayout = qt.QHBoxLayout(self)
        self.hboxlayout.addWidget(self.playback_rate_slider)
        self.hboxlayout.addWidget(self.pan_slider)
        self.hboxlayout.addWidget(self.volume_slider)
        self.hboxlayout.addWidget(self.vboxwidget)

        self.setWindowTitle('Audio Player')
        self.setAcceptDrops(True)

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
        app = qt.QApplication([])

        test_window = TestWindow()
        test_window.show()

        app.exec()

    main()
