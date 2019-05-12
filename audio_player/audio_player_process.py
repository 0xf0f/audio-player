import multiprocessing as mp
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .audio_player import AudioPlayer


class AudioPlayerProcess(mp.Process):
    def __init__(self):
        super().__init__()

        self.daemon = True
        self.command_queue = mp.Queue()

        self.audio_player: 'AudioPlayer' = None

    def process_init(self):
        """
        Called when the child process is starting up.
        Executed inside the child process.
        """
        from .audio_player import AudioPlayer
        self.audio_player = AudioPlayer()
        self.audio_player.resume()

    def run(self) -> None:
        self.process_init()

        while True:
            command, params = self.command_queue.get()

            # print(command, params)

            if command == 'play':
                if params:
                    path = params[0]
                    self.audio_player.set_file(path)

                # player.rewind()
                self.audio_player.resume()

            elif command == 'rewind':
                self.audio_player.rewind()

            elif command == 'pause':
                self.audio_player.pause()

            elif command == 'resume':
                self.audio_player.resume()

            elif command == 'stop':
                self.audio_player.stop()

            elif command == 'toggle':
                if self.audio_player.state == 'playing':
                    self.audio_player.pause()
                else:
                    self.audio_player.resume()

            elif command == 'set_looping':
                self.audio_player.settings.set_looping(params[0])

            elif command == 'set_volume':
                self.audio_player.settings.set_volume(params[0])

            elif command == 'set_pan':
                self.audio_player.settings.set_pan(params[0])

            elif command == 'set_playback_rate':
                self.audio_player.settings.set_playback_rate(params[0])

    def send_command(self, command, *params):
        self.command_queue.put_nowait(
            (command, params)
        )
