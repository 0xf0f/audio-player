import numpy as np
from numba import jit


@jit(nopython=True, nogil=True, parallel=True, cache=True, no_rewrites=True)
def process_vpb(
        data: np.ndarray,
        volume: float,
        pan: float,
        balance: float
):
    if volume != 1:
        data *= volume

    if volume:
        if pan and data.ndim == 2 and data.shape[1] == 2:
            # if data.shape[1] == 1:
            #     data = np.repeat(data[:, np.newaxis], 2, 1)
            abs_pan = abs(pan)
            left: np.ndarray = data[:, 0]
            right: np.ndarray = data[:, 1]

            if pan < 0:
                left, right = right, left

            # right *= 1-(abs_pan/2)
            # right += left*(abs_pan/2)
            right += left*abs_pan
            left *= 1-abs_pan

    return data
