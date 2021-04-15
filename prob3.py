

count = 0


def quick_sort(array):
    def select_idx(pivot_array):
        t, r = divmod(len(pivot_array), 2)
        mid = pivot_array[t] if r else pivot_array[t - 1]
        x = sorted([mid, pivot_array[0], pivot_array[-1]])
        return pivot_array.index(x[1])

    def partition(_a, l_id, r_id):
        global count

        if l_id + 1 >= r_id:
            return _a

        p_id = select_idx(_a[l_id: r_id])
        # preprocess
        _a[l_id + p_id], _a[l_id] = _a[l_id], _a[l_id + p_id]

        count += (r_id - l_id - 1)

        pivot = _a[l_id]
        i = l_id + 1
        for j, num in enumerate(_a[l_id + 1: r_id]):
            if num < pivot:
                _a[j + l_id + 1], _a[i] = _a[i], _a[j + l_id + 1]
                i += 1
        _a[l_id], _a[i - 1] = _a[i - 1], _a[l_id]

        _a = partition(_a, l_id, i - 1)
        _a = partition(_a, i, r_id)

        return _a

    array = partition(array, 0, len(array))
    return array


if __name__ == '__main__':
    with open('data/prob3_data.txt', 'r') as f:

        s = f.readlines()
    s = [int(_s.split()[0]) for _s in s]
    #
    # s = [2, 4, 1, 8]
    s_ = quick_sort(s)
    assert s_ == sorted(s)
    print(count)