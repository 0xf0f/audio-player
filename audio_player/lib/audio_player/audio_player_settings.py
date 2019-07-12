from audio_player.util.settings import SettingList
from audio_player.util.constants.binary_paths import default_soundfont_path


class Settings(SettingList):
    def __init__(self):
        super().__init__()

        self.volume = self.add_setting('volume', 1)
        self.pan = self.add_setting('pan', 0)
        self.playback_rate = self.add_setting('playback_rate', 1)
        self.balance = self.add_setting('balance', 0)
        self.looping = self.add_setting('looping', False)

        self.soundfont = self.add_setting(
            'soundfont', default_soundfont_path
        )
