from .signal import Signal
from types import FunctionType, MethodType
from functools import wraps

# unfinished - do not use

class SignalDescriptor:
    def __init__(self, signal):
        self.signal = signal

    def __get__(self, instance, owner) -> Signal:
        return self.signal

    def __set__(self, instance, value):
        pass

    def __call__(self, *args, **kwargs):
        self.signal(*args, **kwargs)


def signalmethod(method: MethodType):
    def get_signal(self):
        try:
            return getattr(self, f'_{method.__name__}_signal')
        except AttributeError:
            _signal = Signal(method.__name__)
            setattr(self, f'_{method.__name__}_signal', _signal)
            return _signal

    def signal_connect(self, callback):
        return get_signal(self).connect(callback)

    def signal_disconnect(self, callback):
        return get_signal(self).disconnect(callback)

    @property
    def signal_callbacks(self):
        return get_signal(self).callbacks

    @wraps(method)
    def result(self, *args, **kwargs):
        method(self, *args, **kwargs)
        get_signal(self)(*args, **kwargs)

    result.connect = signal_connect
    result.disconnect = signal_disconnect
    result.callbacks = signal_callbacks

    return result


def signalfunction(function: FunctionType):
    _signal = Signal(function.__name__)
    function.__signal__ = _signal

    @wraps(function)
    def result(*args, **kwargs):
        function(*args, **kwargs)
        _signal(*args, **kwargs)

    result.connect = _signal.connect
    result.disconnect = _signal.disconnect
    result.callbacks = _signal.callbacks

    return result
