import numpy as np
from .audio_info.base_object import AudioInfo


# class AudioBlock(np.ndarray):
    # info: 'AudioInfo' = None
    #
    # def __new__(cls, array):
    #     return np.asarray(array).view(cls)
    #
    # def __array_finalize__(self, obj) -> None:
    #     if obj is None:
    #         return
    #
    #     default_attributes = {'info': None}
    #     self.__dict__.update(default_attributes)
    #
    # def __array_ufunc__(self, ufunc, method, *inputs,
    #                     **kwargs):  # this method is called whenever you use a ufunc
    #     f = {
    #         "reduce": ufunc.reduce,
    #         "accumulate": ufunc.accumulate,
    #         "reduceat": ufunc.reduceat,
    #         "outer": ufunc.outer,
    #         "at": ufunc.at,
    #         "__call__": ufunc,
    #     }
    #     output = AudioBlock(f[method](*(i.view(np.ndarray) for i in inputs),
    #                                      **kwargs))  # convert the inputs to np.ndarray to prevent recursion, call the function, then cast it back as ExampleTensor
    #     output.__dict__ = self.__dict__  # carry forward attributes
    #     return output


class AudioBlock:
    def __init__(
        self,
        data: np.ndarray,
        info: AudioInfo,
    ):
        self.data: np.ndarray = data
        self.info: AudioInfo = info

    def copy(self):
        return AudioBlock(
            self.data.copy(),
            self.info,
        )
