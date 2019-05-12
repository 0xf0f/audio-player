from .event_handling import Event


class PlaybackSettings:
    class Events:
        def __init__(self, source: 'PlaybackSettings'):
            self.volume_changed = Event('volume_changed', source)
            self.pan_changed = Event('pan_changed', source)
            self.balance_changed = Event('balance_changed', source)
            self.playback_rate_changed = Event('playback_rate_changed', source)

    def __init__(self):
        self.volume = 1

        # self.left_volume = 1
        # self.right_volume = 1

        self.pan = 0
        self.balance = 0
        self.playback_rate = 1

        self.events = self.__class__.Events(self)

    def set_volume(self, value):
        self.volume = value
        self.events.volume_changed(value)

    def set_pan(self, value):
        self.pan = value
        self.events.pan_changed(value)

    def set_balance(self, value):
        self.balance = value
        self.events.balance_changed(value)

    def set_playback_rate(self, value):
        self.playback_rate = value
        self.events.playback_rate_changed(value)
