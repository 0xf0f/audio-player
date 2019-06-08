from . import qt
import numpy as np
from pathlib import Path

from audio_player.lib import audio_file as af


def max_abs(array: np.ndarray):
    return max(array.max(), abs(array.min()))


class WaveformGenerationThread(qt.QThread):
    update_completed = qt.pyqtSignal()

    def __init__(self, waveform_widget: 'WaveformWidget'):
        super().__init__()
        self.waveform_widget = waveform_widget
        self.pixmap: qt.QPixmap = None
        self.cached_data = None
        self.old_path = None
        self.interrupted = False
        self.frame_interval = 1

    def generate(self):
        width = self.waveform_widget.width()
        height = self.waveform_widget.height()
        path = self.waveform_widget.path

        try:
            file = af.open(path)

        except af.UnableToOpenFileError:
            self.pixmap = None
            self.update_completed.emit()
            return 1

        painter_path = qt.QPainterPath()

        pixmap = qt.QPixmap(width, height)
        pixmap.fill(qt.constants.transparent)

        painter = qt.QPainter(pixmap)
        painter.setRenderHint(painter.Antialiasing)

        if Path(path).stat().st_size > 1024 * 1024 * 5:
            for x in range(0, width, 3):
                if self.interrupted:
                    self.interrupted = False
                    painter.end()
                    return None

                painter_path.addRect(x, height*.25, 1, height*.5)

        else:
            frame_count = file.info.sample_count
            blocks = file.blocks(frame_count//width)

            base_width = width
            width = min(width, frame_count)
            width_scale = width/base_width
            max_value = 0

            center = height/2
            painter_path.moveTo(0, center)

            points = []
            # polygon = qt.QPolygonF()
            # polygon << qt.QPointF(0, center)

            for i, block in enumerate(blocks):
                if self.interrupted:
                    self.interrupted = False
                    painter.end()
                    return None

                block_max = max_abs(block)
                bar_height = abs(block.max()) * height
                bar_bottom = (height-bar_height)/2

                # polygon << qt.QPointF(i, bar_bottom)
                # polygon << qt.QPointF(i, height-bar_bottom)
                painter_path.lineTo(i, bar_bottom)
                points.append((i, height-bar_bottom))

                if block_max > max_value:
                    max_value = block_max

            for x, y in reversed(points):
                painter_path.lineTo(x, y)

            painter_path.lineTo(0, center)

            # companding
            if max_value:
                new_height = height / max_value
                painter.translate(0, -(new_height - height) / 2)
                painter.scale(width_scale, 1 / max_value)

            # painter_path.addPolygon(polygon)

        brush = qt.QBrush()
        brush.setColor(qt.constants.gray)
        brush.setStyle(qt.constants.SolidPattern)
        # painter.drawPolygon(polygon)
        painter.fillPath(painter_path, brush)

        self.pixmap = pixmap
        self.update_completed.emit()
        return 1

    def run(self):
        while not self.generate():
            pass


class WaveformWidget(qt.QWidget):
    def __init__(self):
        super().__init__()
        self.pixmap: qt.QPixmap = None
        self.path = None
        self.waveform_generation_thread = WaveformGenerationThread(self)
        self.waveform_generation_thread.update_completed.connect(self.waveform_updated)
        self.resize_timer = qt.QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.resize_done)

    def waveform_updated(self):
        self.pixmap = self.waveform_generation_thread.pixmap
        self.update()

    def resize_done(self):
        if self.path:
            self.update_pixmap()

    def update_pixmap(self):
        if self.waveform_generation_thread.isRunning():
            self.waveform_generation_thread.interrupted = True
        else:
            self.waveform_generation_thread.start()

    def set_path(self, path):
        self.path = path
        self.update_pixmap()

    def paintEvent(self, event: qt.QPaintEvent):
        if self.pixmap:
            painter = qt.QPainter(self)
            painter.drawPixmap(self.rect(), self.pixmap)

    def resizeEvent(self, event: qt.QResizeEvent):
        self.resize_timer.start(50)
        super().resizeEvent(event)
