from audio_player.lib.signals import Signal
# from collections import deque
from queue import Queue
import threading as th


class PipelineNode:
    def __init__(self, buffer=None):
        if buffer is None:
            buffer = Queue()

        self.buffer = buffer
        self.output = Signal()
        self.input = self.buffer.put

        self.loop_thread = th.Thread(target=self.loop, daemon=True)
        self.loop_thread.start()

    def process_block(self, block):
        return block

    def loop(self):
        while True:
            block = self.buffer.get(block=True)
            block = self.process_block(block)
            self.output(block)

# class Source:
#     pass
#
# class Sink:
#     pass

# class Pipe:
#     def __init__(self, input_queue=None, output_queue=None):
#         if input_queue is None:
#             input_queue = Queue()
#
#         if output_queue is None:
#             output_queue = Queue()
#
#         self.input_queue = input_queue
#         self.output_queue = output_queue
#
#     def write(self, block):
#         self.input_queue.put_nowait(block)
#
#     def process(self, block):
#         return block
#
#     def loop(self):
#         while True:
#             block = self.input_queue.get()
#             block = self.process(block)
#             self.output_queue.put_nowait(block)


# class Pipeline(Pipe):
#     def __init__(self):
#         super().__init__()
#         self.pipes = []
#
#     def add_pipe(self, pipe: AudioPipe):
#         self.pipes.append(pipe)
#
#     def write(self, block):
