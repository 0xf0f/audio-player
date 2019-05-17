from time import monotonic as time


class CodeTimer:
    def __init__(self, name='Timer'):
        self.name = name
        self.t0 = 0
        self.t1 = 0

    def start(self):
        print(self.name, ' - timing...')
        self.t0 = time()

    def finish(self):
        self.t1 = time()
        print(self.name, ' - finished timing')
        print(self.name, ' - time elapsed: ', self.t1-self.t0)

    def print_time(self):
        print(self.name, ' - time elapsed: ', time()-self.t0)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()
