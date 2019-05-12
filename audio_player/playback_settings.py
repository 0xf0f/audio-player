from .event_handling import EventEmitter


class PlaybackSettings(EventEmitter):
    def __init__(self):
        self.volume = 1

        # self.left_volume = 1
        # self.right_volume = 1

        self.pan = 0
        self.balance = 0
        self.playback_rate = 1

    def set_volume(self, value):
        self.volume = value
        self.event('volume_changed', value)

    def set_pan(self, value):
        self.pan = value
        self.event('pan_changed', value)

    def set_balance(self, value):
        self.balance = value
        self.event('balance_changed', value)

    def set_playback_rate(self, value):
        self.playback_rate = value
        self.event('playback_rate_changed', value)
