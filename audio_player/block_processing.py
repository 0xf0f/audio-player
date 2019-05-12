import numpy as np
from numba import jit


@jit(nopython=True, nogil=True, parallel=True)
def process_block(
        data: np.ndarray,
        volume: float,
        pan: float,
        balance: float
):
    if volume != 1:
        data *= volume

    if volume:
        if pan:
            abs_pan = abs(pan)
            left: np.ndarray = data[:, 0]
            right: np.ndarray = data[:, 1]

            if pan < 0:
                left, right = right, left

            right *= 1-(abs_pan/2)
            right += left*(abs_pan/2)
            left *= 1-abs_pan

    return data
