from inspect import ismethod
from .weak_method_set import WeakMethodSet


class Signal:
    def __init__(self, name=None):
        super().__init__()

        self.name = name

        self.callback_methods = WeakMethodSet()
        self.callback_functions = set()

    @property
    def callbacks(self):
        yield from self.callback_methods
        yield from self.callback_functions

    def connect(self, callback):
        if ismethod(callback):
            self.callback_methods.add(callback)
        else:
            self.callback_functions.add(callback)

    def disconnect(self, callback):
        if ismethod(callback):
            self.callback_methods.discard(callback)
        else:
            self.callback_functions.discard(callback)

    def __call__(self, *args, **kwargs):
        self.emit(*args, **kwargs)

    def __str__(self):
        return f'<Signal {self.name}>'

    def propagate_callbacks(self, *args, **kwargs):
        for callback in self.callback_methods:
            callback(*args, **kwargs)

        for callback in self.callback_functions:
            callback(*args, **kwargs)

    emit = propagate_callbacks
