from audio_player.lib.signals import Signal
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
