import time
import numpy as np
import threading as th
from typing import List, Union, Dict

from .audio_player_settings import Settings as AudioPlayerSettings
from .audio_player_signals import Signals as AudioPlayerSignals
from .audio_player_states import States as AudioPlayerStates

from ..audio_source import AudioSource
from ..audio_sink.base_object import AudioSink
from ..audio_sink.sounddevice_sink import SoundDeviceSink

from ..audio_block import AudioBlock

import audio_player.lib.audio_file as af
from audio_player.lib.audio_file.base_object import AudioFile

# from ..audio_pipeline import Pipeline
from ..audio_pipeline import PipelineNode
from ..audio_pipeline import Pipeline

from samplerate import Resampler
from ..audio_processing import process_vpb

class AudioPlayer:
    States = AudioPlayerStates

    def __init__(self):
        # self.output_cache = AudioOutputCache()
        # self.file: AudioFile = None
        #
        self.signals = AudioPlayerSignals()
        self.settings = AudioPlayerSettings()

        self.paused = th.Event()
        self.play_lock = th.Lock()
        # self.read_lock = th.Lock()

        # self.audio_pipeline = PipelineNode()
        # self.audio_pipeline.buffer.maxsize = 1
        # self.audio_pipeline.output.connect(self.write_block)

        # self.block_buffer = Queue()
        # self.block_buffer.maxsize = 1

        self.state = AudioPlayer.States.stopped

        self.source: AudioSource = None
        self.pipeline: Pipeline = None
        self.sinks: List[AudioSink] = [SoundDeviceSink()]
        self.loop_thread = th.Thread(target=self.loop, daemon=True)
        self.loop_thread.start()

        self.resamplers: Dict[int, Resampler] = dict()


    # def get_output(self, samplerate, channels):
    #     try:
    #         return self.output_cache[samplerate, channels]
    #
    #     except KeyError:
    #         new_output = AudioOutput(samplerate, channels, self.settings)
    #         new_output.start()
    #
    #         self.output_cache[samplerate, channels] = new_output
    #         return new_output

    # def audio_loop(self):
    #     # silence = AudioBlock(
    #     #     np.silence((4096, 2), dtype='float32'),
    #     #     44100
    #     # )
    #
    #     while True:
    #         # try:
    #         #     block = self.block_buffer.get_nowait()
    #         # except Empty:
    #         #     block = silence
    #
    #         block = self.block_buffer.get()
    #         self.audio_pipeline.input(block)

    # def read_loop(self):
    #     # block = np.silence()
    #     while True:
    #         self.paused.wait()
    #         file = self.file
    #         if file:
    #             # start_time = self.file.tell_time()
    #             self.signals.position_changed.emit(
    #                 file.tell_time()
    #             )
    #             block = file.read(4096)
    #             # print('file', block.size)
    #             # end_time = self.file.tell_time()
    #
    #             if not block.size:
    #                 if self.settings.looping.get():
    #                     file.seek_time(0)
    #                     block = file.read(4096)
    #                 else:
    #                     # print('file exhausted')
    #                     self.stop()
    #                     continue
    #
    #             self.block_buffer.put(
    #                 AudioBlock(
    #                     block,
    #                     file.info.sample_rate
    #                 )
    #             )
    #
    #         else:
    #             self.stop()
    #             continue
    #
    # def write_block(self, block: AudioBlock):
    #     # self.paused.wait()
    #
    #     # self.signals.position_changed(
    #     #     block.start_time
    #     # )
    #
    #     self.get_output(
    #         block.sample_rate,
    #         block.channels
    #     ).write(block.data)
    #
    #     # self.signals.position_changed(
    #     #     block.end_time
    #     # )
    #
    # def set_file(self, path, clear_buffer=True):
    #     try:
    #         self.file = af.open(path)
    #         self.signals.source_changed(path)
    #         self.signals.duration_changed(self.file.info.duration)
    #
    #         if clear_buffer:
    #             self.audio_pipeline.clear_buffer()
    #
    #         return True
    #
    #     except af.UnableToOpenFileError:
    #         return False
    #
    #         # self.file = None
    #         # self.signals.source_changed(None)
    #         # self.signals.duration_changed(0)

    def loop(self):
        while True:
            self.paused.wait()
            source = self.source
            if source:
                self.signals.position_changed.emit(
                    self.source.tell_time()
                )
                data = source.read(4096)
                # data = info.read(64)

                if not data.size:
                    if self.settings.looping.get():
                        source.seek_time(0)
                        data = source.read(4096)
                    else:
                        self.stop()
                        continue

                block = AudioBlock(data, source.info)

                if self.pipeline:
                    self.pipeline.input(block)
                else:
                    self.play_block(block)

            else:
                self.stop()
                continue

    def set_source(self, source: AudioSource):
        self.source = source
        if isinstance(source, AudioFile):
            self.signals.file_changed.emit(source.path)
        else:
            self.signals.file_changed.emit(None)

        self.signals.source_changed.emit(f'{source}')
        self.signals.duration_changed.emit(source.info.duration)

    def set_state(self, state):
        if self.state != state:
            self.state = state
            self.signals.state_changed(state)

    def play(self, source: Union[AudioSource, str]=None):
        if source:
            if isinstance(source, str):
                try:
                    source = af.open(source)
                except af.UnableToOpenFileError:
                    return

            self.set_source(source)

        self.resume()

    def get_resampler(self, channels):
        try:
            return self.resamplers[channels]
        except KeyError:
            resampler = Resampler(channels=channels)
            self.resamplers[channels] = resampler
            return resampler

    def play_block(self, block: AudioBlock):
        with self.play_lock:

            volume = self.settings.volume.get()
            pan = self.settings.pan.get()
            balance = self.settings.balance.get()
            playback_rate = self.settings.playback_rate.get()
            resampling_ratio = 1/playback_rate

            block.data = process_vpb(
                block.data,
                volume,
                pan,
                balance
            )

            if playback_rate != 1:
                block.data = self.get_resampler(
                    block.info.channels
                ).process(
                    block.data,
                    ratio=resampling_ratio
                )

            for sink in self.sinks:
                sink.write(block)

    def toggle(self):
        if self.state == AudioPlayer.States.playing:
            self.pause()
        else:
            self.resume()

    def stop(self):
        self.paused.clear()

        # if clear_buffer:
        #     self.audio_pipeline.clear_buffer()

        if self.source:
            self.source.seek_time(0)
            self.signals.position_changed(0)

        self.set_state(AudioPlayer.States.stopped)

    def resume(self):
        self.paused.set()
        self.set_state(AudioPlayer.States.playing)

    def pause(self):
        self.paused.clear()

        # if clear_buffer:
        #     self.audio_pipeline.clear_buffer()

        self.set_state(AudioPlayer.States.paused)

    def rewind(self):
        self.seek_time(0)

    def seek_time(self, seconds):
        if self.source:
            self.source.seek_time(seconds)

            # if clear_buffer:
            #     self.audio_pipeline.clear_buffer()

    def wait(self, extra_time=.5):
        # wait til player stops
        # this is a placeholder, needs to be rewritten

        event = th.Event()

        # def wait_for_stop():
        #     for output in self.output_cache:
        #         output.stream.

        self.signals.state_changed.connect(
            lambda state: event.set() if state == self.States.stopped else None
        )

        event.wait()
        # print('done')
        if self.pipeline:
            self.pipeline.wait()
        time.sleep(extra_time)
        # print('finished')
