import threading as th
from queue import Queue
from audio_player.util.signals import Signal


class PipelineNode:
    def __init__(self, buffer: Queue = None):
        if buffer is None:
            buffer = Queue()
            buffer.maxsize = 1

        self.buffer = buffer
        self.output = Signal()
        self.input = self.buffer.put

        self.loop_thread = th.Thread(target=self.loop, daemon=True)
        # self.loop_thread.start()

    def clear_buffer(self):
        # https://stackoverflow.com/a/31892187/10444096
        with self.buffer.mutex:
            unfinished = self.buffer.unfinished_tasks - len(self.buffer.queue)
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.buffer.all_tasks_done.notify_all()
            self.buffer.unfinished_tasks = unfinished
            self.buffer.queue.clear()
            self.buffer.not_full.notify_all()

    def process_block(self, block):
        return block

    def loop(self):
        while True:
            block = self.buffer.get()
            block = self.process_block(block)
            self.buffer.task_done()
            self.output(block)

    def start(self):
        self.loop_thread.start()

    def set_buffer_size(self, size):
        self.buffer.maxsize = size

    def connect_to(self, callback):
        self.output.connect(callback)

    def wait(self):
        self.buffer.join()

    def __call__(self, item):
        self.buffer.put(item)
