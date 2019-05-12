#scrapped

def default_event_callback(source, name, *args, **kwargs):
    pass


class EventConnector:
    def __init__(self, source: 'EventEmitter', name):
        self.source = source
        self.name = name

    def connect(self, *targets):
        if not self.source.event_connections:
            self.source.event_connections = dict()

        # try:
        #     event_connections_list =

    def __call__(self, *args, **kwargs):
        self.source.event(self.name, *args, **kwargs)


class EventEmitter:
    event_callback = default_event_callback
    event_connections: dict = None

    def event(self, name, *args, **kwargs):
        self.event_callback(name, *args, **kwargs)

    def set_event_callback(self, callback: callable):
        self.event_callback = callback

    def on_event(self, name):
        return EventConnector(self, name)