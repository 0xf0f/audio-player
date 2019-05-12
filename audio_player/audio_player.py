import threading as th
import time

from .audio_output import AudioOutput
from .audio_output_cache import AudioOutputCache

from .audio_buffer import AudioBuffer
from .audio_buffer_cache import AudioBufferCache
from .audio_buffer_cache import ExceedsCacheSize

from .audio_player_settings import AudioFilePlayerSettings

from .event_handling import EventEmitter

from audioread.exceptions import DecodeError


class AudioPlayer(EventEmitter):
    active_buffer: AudioBuffer

    def __init__(self):
        self.output_cache = AudioOutputCache()
        self.buffer_cache = AudioBufferCache()
        self.active_buffer: AudioBuffer = None

        self.settings = AudioFilePlayerSettings()

        self.paused = th.Event()

        self.play_loop_thread = th.Thread(target=self.play_loop, daemon=True)
        self.play_loop_thread.start()

    def set_file(self, path):
        active_buffer = self.active_buffer

        if path:
            try:
                new_active_buffer = self.buffer_cache.get(path)
            except KeyError:
                try:
                    new_active_buffer = AudioBuffer(path)

                except DecodeError:
                    new_active_buffer = None


            # self.get_output(
            #     new_active_buffer.file.samplerate,
            #     new_active_buffer.file.channels
            # )

            if new_active_buffer:
                new_active_buffer.seek(0)

            self.active_buffer = new_active_buffer

        else:
            self.active_buffer = None

        if active_buffer:
            try:
                self.buffer_cache.put(
                    active_buffer.path,
                    active_buffer
                )
            except ExceedsCacheSize:
                pass

    def get_output(self, samplerate, channels):
        try:
            return self.output_cache[samplerate, channels]

        except KeyError:
            new_output = AudioOutput(samplerate, channels, self.settings)
            new_output.start()

            self.output_cache[samplerate, channels] = new_output
            return new_output

    def play_loop(self):
        while True:
            self.paused.wait()

            buffer = self.active_buffer

            if buffer:
                if buffer.file_exhausted and buffer.tell() == len(buffer):
                    if self.settings.looping:
                        buffer.seek(0)
                    else:
                        self.stop()
                        continue

                chunk = buffer.read(4096, numpy_array=True)

                output = self.get_output(
                    buffer.file.samplerate,
                    buffer.file.channels
                )

                samplerate = buffer.file.samplerate
                samples_written = output.write(chunk)

                time.sleep(samples_written / samplerate / 2)

            else:
                self.stop()
                continue

    def play(self, path):
        self.set_file(path)
        self.event('file_changed', path)

        self.paused.set()
        self.event('state_changed', 'playing')

    def stop(self):
        self.paused.clear()

        if self.active_buffer:
            self.active_buffer.seek(0)

        self.event('state_changed', 'stopped')
        # self.set_file(None)

    def resume(self):
        self.paused.set()
        self.event('state_changed', 'playing')

    def pause(self):
        self.paused.clear()
        self.event('state_changed', 'paused')

    def rewind(self):
        if self.active_buffer:
            self.active_buffer.seek(0)

