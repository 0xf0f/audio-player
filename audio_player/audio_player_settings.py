from .playback_settings import PlaybackSettings
from .event_handling import Event


class AudioFilePlayerSettings(PlaybackSettings):
    events: 'AudioFilePlayerSettings.Events'

    class Events(PlaybackSettings.Events):
        def __init__(self, source: 'AudioFilePlayerSettings'):
            super().__init__(source)
            self.looping_changed = Event('looping_changed', source)

    def __init__(self):
        super().__init__()
        self.looping = False

    def set_looping(self, value):
        self.looping = value
        self.events.looping_changed(value)
