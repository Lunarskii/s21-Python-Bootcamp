import time
from mul import mul as py_mul
from multiply import mul as cy_mul


x = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
y = [[1, 2], [1, 2], [3, 4]]
expected_result = [[12, 18], [27, 42], [42, 66], [57, 90]]


def mark_time(func):
    start_time = time.time()
    assert func(x, y) == expected_result
    end_time = time.time()
    return (end_time - start_time) * 1000


if __name__ == '__main__':
    py_mul_time = round(mark_time(py_mul), 6)
    cy_mul_time = round(mark_time(cy_mul), 6)
    time_diff = round(abs(cy_mul_time - py_mul_time), 6)
    print(f'Python Mul: {py_mul_time}ms')
    print(f'Cython Mul: {cy_mul_time}ms')

    if cy_mul_time < py_mul_time:
        print(f'Cython faster than Python in {time_diff}ms',)
    else:
        print(f'Python faster than Cython in {time_diff}ms')
