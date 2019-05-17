import multiprocessing as mp
from .audio_player import AudioPlayer


class AudioPlayerProcess(mp.Process):
    def __init__(self):
        super().__init__()

        self.daemon = True
        self.command_queue = mp.Queue()
        self.signal_queue = mp.Queue()

        self.audio_player: 'AudioPlayer' = None
        self.command_map: dict = None

    def process_init(self):
        """
        Called when the child process is starting up.
        Executed inside the child process.
        """

        self.audio_player = AudioPlayer()

        def pipe_to_queue(signal_name):
            return lambda *args, **kwargs: self.signal_queue.put_nowait(
                (signal_name, args, kwargs)
            )

        for signal in self.audio_player.signals:
            signal.connect(pipe_to_queue(signal.name))

        for setting in self.audio_player.settings:
            setting.changed.emit = lambda *args, **kwargs: None

        self.command_map = {
            'play': self.audio_player.play,
            'toggle': self.audio_player.toggle,
            'stop': self.audio_player.stop,
            'resume': self.audio_player.resume,
            'pause': self.audio_player.pause,
            'rewind': self.audio_player.rewind,
            'seek_time': self.audio_player.seek_time,

            'set_volume': self.audio_player.settings.volume.set,
            'set_pan': self.audio_player.settings.pan.set,
            'set_balance': self.audio_player.settings.balance.set,
            'set_playback_rate': self.audio_player.settings.playback_rate.set,
            'set_looping': self.audio_player.settings.looping.set
        }

        self.audio_player.resume()

    def run(self) -> None:
        from audio_player.lib.code_timer import CodeTimer

        with CodeTimer('process init'):
            self.process_init()

        while True:
            command, args = self.command_queue.get()
            # print(command, args)
            command = self.command_map.get(command, lambda *args, **kwargs: None)
            command(*args)
