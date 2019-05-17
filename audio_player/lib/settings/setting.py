from ..signals import Signal


class Setting:
    changed: Signal

    def __init__(self, name, default=None):
        self.name = name
        self.changed: Signal = Signal(f'{name}_changed')
        self.value = default

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        self.changed.emit(value)

    def __iadd__(self, value):
        self.set(self.value + value)

    def __isub__(self, value):
        self.set(self.value - value)

    def __imul__(self, value):
        self.set(self.value * value)

    def __idiv__(self, value):
        self.set(self.value * value)
