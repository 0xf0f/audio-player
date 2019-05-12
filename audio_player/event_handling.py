from weakref import ref
from .weak_method_set import WeakMethodSet
from inspect import ismethod
import multiprocessing as mp


class EventData:
    pass


def default_event_emission(event: 'Event', *args, **kwargs):
    event.propagate_callbacks(*args, **kwargs)


class Event:
    emit = default_event_emission
    source = None

    def __init__(self, name=None, source=None):
        super().__init__()

        self.name = name

        if source is not None:
            self.source = ref(source)

        self.callback_methods = WeakMethodSet()
        self.callback_functions = set()

    @property
    def callbacks(self):
        yield from self.callback_methods
        yield from self.callback_functions

    def register_callback(self, callback):
        if ismethod(callback):
            self.callback_methods.add(callback)

        else:
            self.callback_functions.add(callback)

    def unregister_callback(self, callback):
        if ismethod(callback):
            self.callback_methods.discard(callback)

        else:
            self.callback_functions.discard(callback)

    def __call__(self, *args, **kwargs):
        self.emit(*args, **kwargs)

    def propagate_callbacks(self, *args, **kwargs):
        for callback in self.callback_methods:
            callback(self, *args, **kwargs)

        for callback in self.callback_functions:
            callback(self, *args, **kwargs)


# class EventQueue:
#     def __init__(self, base_type=mp.Queue):
#         self.queue = base_type()
#
#     def push(self, ):

class EventList:
    def __init__(self, source):
        self.source = source
        self.events = []

    def add_event(self, name):
        event = Event(name, self.source)
        self.events.append(event)
        return event

    def __iter__(self):
        yield from self.events

if __name__ == '__main__':
    class MouseEnteredEventData(EventData):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class MouseEnteredEvent(Event):
        def __init__(self):
            super().__init__()

        def __call__(self, x, y):
            super().__call__(
                MouseEnteredEventData(x, y)
            )

    def test(event_data: MouseEnteredEventData):
        print(event_data.x, event_data.y)

    mouse_entered = MouseEnteredEvent()
    mouse_entered.register_callback(test)
    mouse_entered(0, 0)



