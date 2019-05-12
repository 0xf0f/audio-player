import multiprocessing as mp


class AudioPlayerProcess(mp.Process):
    def __init__(self):
        super().__init__()

        self.daemon = True
        self.command_queue = mp.Queue()

    def run(self) -> None:
        from .event_handling import EventEmitter
        EventEmitter.event_callback = (
            lambda source, name, *args, **kwargs: print(source, name, args, kwargs)
        )

        from audio_player import AudioPlayer
        player = AudioPlayer()
        player.resume()

        while True:
            command, params = self.command_queue.get()

            print(command, params)

            if command == 'play':
                if params:
                    path = params[0]
                    player.set_file(path)

                # player.rewind()
                player.resume()

            elif command == 'rewind':
                player.rewind()

            elif command == 'pause':
                player.pause()

            elif command == 'resume':
                player.resume()

            elif command == 'stop':
                player.pause()
                player.rewind()

            elif command == 'set_looping':
                player.settings.set_looping(params[0])

            elif command == 'set_volume':
                player.settings.set_volume(params[0])

            elif command == 'set_pan':
                player.settings.set_pan(params[0])

            elif command == 'set_playback_rate':
                player.settings.set_playback_rate(params[0])

    def send_command(self, command, *params):
        self.command_queue.put_nowait(
            (command, params)
        )
