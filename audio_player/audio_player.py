import threading as th

from .audio_output import AudioOutput
from .audio_output_cache import AudioOutputCache

from audio_player.lib import audio_file as af
from audio_player.lib.audio_file.audio_file import AudioFile

from .audio_player_settings import Settings as AudioPlayerSettings
from .audio_player_signals import Signals as AudioPlayerSignals
from .audio_player_states import States as AudioPlayerStates


class AudioPlayer:
    class States(AudioPlayerStates):
        pass

    def __init__(self):
        self.output_cache = AudioOutputCache()
        self.file: AudioFile = None

        self.signals = AudioPlayerSignals()
        self.settings = AudioPlayerSettings()

        self.paused = th.Event()

        self.audio_loop_thread = th.Thread(target=self.audio_loop, daemon=True)
        self.audio_loop_thread.start()

        self.state = AudioPlayer.States.stopped

    def set_file(self, path):
        try:
            self.file = af.open(path)
            self.signals.file_changed(path)
            self.signals.duration_changed(self.file.info.duration)

        except af.UnableToOpenFileError:
            self.file = None
            self.signals.file_changed(None)
            self.signals.duration_changed(0)

    def get_output(self, samplerate, channels):
        try:
            return self.output_cache[samplerate, channels]

        except KeyError:
            new_output = AudioOutput(samplerate, channels, self.settings)
            new_output.start()

            self.output_cache[samplerate, channels] = new_output
            return new_output

    def audio_loop(self):
        # block = np.empty()
        while True:
            self.paused.wait()
            file = self.file
            if file:
                self.signals.position_changed(
                    file.tell_time()
                )

                block = self.file.read(4096)

                if not block.size:
                    if self.settings.looping.get():
                        self.file.seek_time(0)
                        block = self.file.read(4096)
                    else:
                        self.stop()
                        continue

                self.get_output(
                    file.info.sample_rate,
                    file.info.channels

                ).write(block)

            else:
                self.stop()
                continue

    def set_state(self, state):
        if self.state != state:
            self.state = state
            self.signals.state_changed(state)

    def play(self, path=None):
        self.set_file(path)
        self.signals.file_changed(path)

        self.paused.set()
        self.set_state(AudioPlayer.States.playing)

    def toggle(self):
        if self.state == AudioPlayer.States.playing:
            self.pause()
        else:
            self.resume()

    def stop(self):
        self.paused.clear()

        if self.file:
            self.file.seek_time(0)
            self.signals.position_changed(0)

        self.set_state(AudioPlayer.States.stopped)

    def resume(self):
        self.paused.set()
        self.set_state(AudioPlayer.States.playing)

    def pause(self):
        self.paused.clear()
        self.set_state(AudioPlayer.States.paused)

    def rewind(self):
        if self.file:
            self.file.seek_time(0)

    def seek_time(self, seconds):
        if self.file:
            self.file.seek_time(seconds)
