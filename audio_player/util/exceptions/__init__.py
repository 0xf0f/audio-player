class UnableToOpenFileError(Exception):
    def __init__(self, path):
        super().__init__(f'Error occurred while opening {path}')