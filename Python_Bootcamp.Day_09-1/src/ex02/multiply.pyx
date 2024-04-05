from itertools import tee


cpdef list mul(list a, list b):
    cdef list b_iter = list(tee(zip(*b), len(a)))
    cdef list result = [], result_row
    cdef int i, j
    cdef int sum_val

    for i, row_a in enumerate(a):
        result_row = []
        for j, col_b in enumerate(b_iter[i]):
            sum_val = 0
            for ele_a, ele_b in zip(row_a, col_b):
                sum_val += <int>ele_a * <int>ele_b
            result_row.append(sum_val)
        result.append(result_row)

    return result
