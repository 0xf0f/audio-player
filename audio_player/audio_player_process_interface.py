# from .audio_player import AudioPlayer
from .audio_player_process import AudioPlayerProcess
import threading as th

from .audio_player_settings import Settings as AudioPlayerSettings
from .audio_player_signals import Signals as AudioPlayerSignals
from .audio_player_states import States as AudioPlayerStates


class AudioPlayerProcessInterface:
    process = None

    class States(AudioPlayerStates):
        pass

    class Settings(AudioPlayerSettings):
        def __init__(self, controller: 'AudioPlayerProcessInterface'):
            super().__init__()

            self.controller = controller

            def pipe_to_command(setting_name):
                return lambda *args, **kwargs: self.controller.send_command(
                    f'set_{setting_name}', *args
                )

            for setting in self:
                setting.changed.connect(
                    pipe_to_command(setting.name)
                )

    class Signals(AudioPlayerSignals):
        pass

    class SignalThread(th.Thread):
        def __init__(self, controller: 'AudioPlayerProcessInterface'):
            super().__init__()
            self.signals = controller.signals
            self.signal_queue = controller.process.signal_queue
            self.daemon = True

        def run(self) -> None:
            while True:
                signal, args, kwargs = self.signal_queue.get()
                # print(signal, args, kwargs)
                self.signals[signal](*args, **kwargs)

    def __init__(self):
        self.signals = AudioPlayerProcessInterface.Signals()
        self.settings = AudioPlayerProcessInterface.Settings(self)

        self.process = AudioPlayerProcess()
        self.command_queue = self.process.command_queue
        # self.process.start()

        self.signal_thread = AudioPlayerProcessInterface.SignalThread(self)
        self.signal_thread.start()

    def __del__(self):
        if self.process:
            self.process.terminate()

    def start_process(self):
        self.process.start()

    def send_command(self, command, *args):
        self.command_queue.put_nowait(
            (command, args)
        )

    def play(self, path=None):
        self.send_command('play', path)

    def toggle(self):
        self.send_command('toggle')

    def stop(self):
        self.send_command('stop')

    def resume(self):
        self.send_command('resume')

    def pause(self):
        self.send_command('pause')

    def rewind(self):
        self.send_command('rewind')

    def seek_time(self, seconds):
        self.send_command('seek_time', seconds)
