from audio_player.util.signals import Signal
from queue import Queue
import threading as th


class PipelineBuffer(Queue):
    def clear(self):
        # https://stackoverflow.com/a/31892187/10444096
        with self.mutex:
            unfinished = self.unfinished_tasks - len(self.queue)
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished
            self.queue.clear()
            self.not_full.notify_all()


class PipelineNode:
    def __init__(self, buffer: Queue=None):
        if buffer is None:
            buffer = Queue()

        self.buffer = buffer
        self.output = Signal()
        self.input = self.buffer.put

        self.loop_thread = th.Thread(target=self.loop, daemon=True)
        self.loop_thread.start()

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
            self.output(block)


class PipelineNodeV2:
    def __init__(self, buffer: Queue=None):
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
            self.output(block)

    def start(self):
        self.loop_thread.start()

    def set_buffer_size(self, size):
        self.buffer.maxsize = size

    def connect_to(self, callback):
        self.output.connect(callback)

    def __call__(self, item):
        self.buffer.put(item)


class AudioSourceNode(PipelineNodeV2):
    pass


class AudioSinkNode(PipelineNodeV2):
    pass

# class Pipeline(PipelineNode):
#     pass

# class PipelineNode:
#     def __init__(self):
#         self.loop_thread = th.Thread(target=self.loop, daemon=True)
#
#     def loop(self):
#         pass
#
#
# class InputNode(PipelineNode):
#     def __init__(self):
#         super().__init__()
#
#         self.buffer = Queue()
#         self.input = self.buffer.put
#
#
# class OutputNode(PipelineNode):
#     def __init__(self):
#         super().__init__()
#
#         self.output = Signal('output')
#
#
# class ProducerNode(OutputNode):
#     def produce_items(self):
#         yield from ()
#
#     def loop(self):
#         # while True:
#         for item in self.produce_items():
#             self.output(item)
#
#
# class ProcessorNode(InputNode, OutputNode):
#     def process_item(self, item):
#         yield item
#
#     def loop(self):
#         while True:
#             unprocessed_item = self.buffer.get()
#             for result in self.process_item(unprocessed_item):
#                 self.output(result)
#
#
# class ConsumerNode(InputNode):
#     def consume_item(self, item):
#         pass
#
#     def loop(self):
#         while True:
#             item = self.buffer.get()
#             self.consume_item(item)
