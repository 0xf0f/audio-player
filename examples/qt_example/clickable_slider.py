import qt


class ClickableSlider(qt.QSlider):
    position_updated = qt.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.mouse_down = False

    def mousePressEvent(self, event: qt.QMouseEvent):
        if self.orientation() == qt.Constants.Horizontal:
            self.setValue(qt.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))
        else:
            self.setValue(qt.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.y(), self.height(), True))
        self.mouse_down = True

    def mouseReleaseEvent(self, event: qt.QMouseEvent):
        self.mouse_down = False
        self.position_updated.emit(self.value())

    def mouseMoveEvent(self, event: qt.QMouseEvent):
        if self.orientation() == qt.Constants.Horizontal:
            self.setValue(qt.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))
        else:
            self.setValue(qt.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.y(), self.height(), True))
