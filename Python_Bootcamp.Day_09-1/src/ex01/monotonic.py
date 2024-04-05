from time import CLOCK_MONOTONIC
import ctypes
import ctypes.util


def monotonic():
    libc = ctypes.CDLL(ctypes.util.find_library('c'))
    clock_gettime = libc.clock_gettime
    clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_long)]
    timespec = (ctypes.c_long * 2)()
    clock_gettime(CLOCK_MONOTONIC, timespec)
    return timespec[0] + timespec[1] * 1e-9


if __name__ == '__main__':
    print(monotonic())
