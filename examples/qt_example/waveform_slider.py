from . import qt
from .waveform_widget import WaveformWidget
from .clickable_slider import ClickableSlider

slider_color = qt.QColor(100, 100, 100)


class WaveformSlider(ClickableSlider, WaveformWidget):
    def __init__(self):
        super().__init__()
        self.setOrientation(qt.constants.Horizontal)
        self.setMaximum(100)
        # self.setFixedHeight(64)
        self.setFixedHeight(96)

    def paintEvent(self, event: qt.QPaintEvent):
        WaveformWidget.paintEvent(self, event)
        painter = qt.QPainter(self)
        painter.setCompositionMode(painter.CompositionMode_Difference)
        if self.maximum() > 0:
            painter.fillRect(
                int(self.sliderPosition() / self.maximum() * self.width())-2,
                0, 4, self.height(), slider_color
            )