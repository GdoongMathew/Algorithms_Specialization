import numpy as np

def count_inversion(a, num_inv):
    if len(a) == 2:
        if a[0] > a[1]:
            num_inv += 1
            return a[::-1], num_inv
        else:
            return a, num_inv
    elif len(a) == 1:
        return a, num_inv

    mid_idx = int(len(a) / 2)
    l_a, r_a = a[: mid_idx], a[mid_idx:]

    # get sorted left and right half of the array
    l_a, l_inv = count_inversion(l_a, num_inv)
    r_a, r_inv = count_inversion(r_a, num_inv)

    num_inv += (l_inv + r_inv)

    # merge and count
    final_a = []
    l_i, r_i = 0, 0
    while l_i < len(l_a) or r_i < len(r_a):
        if l_i == len(l_a) and r_a[r_i:]:
            final_a.extend(r_a[r_i:])
            break
        if r_i == len(r_a) and l_a[l_i:]:
            # num_inv += len(l_a[l_i + 1:]) * r_i
            final_a.extend(l_a[l_i:])
            break
        next_l = -np.inf if l_i == len(l_a) else l_a[l_i]
        next_r = np.inf if r_i == len(r_a) else r_a[r_i]

        if next_l > next_r:
            final_a.append(next_r)
            num_inv += (len(l_a[l_i:]))
            r_i += 1
        else:
            # next_r >= next_l
            final_a.append(next_l)
            l_i += 1

    return final_a, num_inv


def mergeSort(arr, n):
    # A temp_arr is created to store
    # sorted array in merge function
    temp_arr = [0] * n
    return _mergeSort(arr, temp_arr, 0, n - 1)


# This Function will use MergeSort to count inversions

def _mergeSort(arr, temp_arr, left, right):
    # A variable inv_count is used to store
    # inversion counts in each recursive call

    inv_count = 0

    # We will make a recursive call if and only if
    # we have more than one elements

    if left < right:
        # mid is calculated to divide the array into two subarrays
        # Floor division is must in case of python

        mid = (left + right) // 2

        # It will calculate inversion
        # counts in the left subarray

        inv_count += _mergeSort(arr, temp_arr,
                                left, mid)

        # It will calculate inversion
        # counts in right subarray

        inv_count += _mergeSort(arr, temp_arr,
                                mid + 1, right)

        # It will merge two subarrays in
        # a sorted subarray

        inv_count += merge(arr, temp_arr, left, mid, right)
    return inv_count


# This function will merge two subarrays
# in a single sorted subarray
def merge(arr, temp_arr, left, mid, right):
    i = left  # Starting index of left subarray
    j = mid + 1  # Starting index of right subarray
    k = left  # Starting index of to be sorted subarray
    inv_count = 0

    # Conditions are checked to make sure that
    # i and j don't exceed their
    # subarray limits.

    while i <= mid and j <= right:

        # There will be no inversion if arr[i] <= arr[j]

        if arr[i] <= arr[j]:
            temp_arr[k] = arr[i]
            k += 1
            i += 1
        else:
            # Inversion will occur.
            temp_arr[k] = arr[j]
            inv_count += (mid - i + 1)
            k += 1
            j += 1

    # Copy the remaining elements of left
    # subarray into temporary array
    while i <= mid:
        temp_arr[k] = arr[i]
        k += 1
        i += 1

    # Copy the remaining elements of right
    # subarray into temporary array
    while j <= right:
        temp_arr[k] = arr[j]
        k += 1
        j += 1

    # Copy the sorted subarray into Original array
    for loop_var in range(left, right + 1):
        arr[loop_var] = temp_arr[loop_var]

    return inv_count


if __name__ == '__main__':
    with open('data/prob2_data.txt', 'r') as f:

        s = f.readlines()
    s = [int(_s.split()[0]) for _s in s]

    # s = [1, 20, 6, 4, 5]

    _, x = count_inversion(s, 0)
    print(x)
    x = mergeSort(s, len(s))
    print(x)

