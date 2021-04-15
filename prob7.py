from numpy import inf


class Heap:
    def __init__(self, method='max'):
        assert method in ['max', 'min']
        self._method = method
        self._elements = []

    def heapify(self, elements):
        for element in elements:
            self.insert(element)

    @ property
    def root(self):
        if len(self._elements):
            return self._elements[0]
        elif self._method == 'max':
            return inf
        else:
            return -inf


    def parent_idx(self, idx):
        return int((idx - 1) / 2)

    def child_idx(self, idx):
        l_idx = 2 * idx + 1
        return l_idx, l_idx + 1

    def swap(self, f_idx, s_idx):
        self._elements[f_idx], self._elements[s_idx] = self._elements[s_idx], self._elements[f_idx]

    def condition(self, p_idx, c_idx):
        if self._method == 'min':
            return self._elements[p_idx] <= self._elements[c_idx]

        else:
            return self._elements[p_idx] >= self._elements[c_idx]

    def insert(self, element):

        def _bobble_up(_idx):
            _p_idx = self.parent_idx(_idx)
            self.swap(_p_idx, _idx)
            return _p_idx

        self._elements.append(element)
        ele_idx = len(self._elements) - 1
        parent_idx = self.parent_idx(ele_idx)

        if ele_idx != 0:
            while not self.condition(parent_idx, ele_idx):
                ele_idx = _bobble_up(ele_idx)
                parent_idx = self.parent_idx(ele_idx)

    def extract(self):
        self.swap(0, len(self._elements) - 1)
        root = self._elements.pop()

        parent_idx = 0

        def select_child(p_idx):

            l_idx, r_idx = self.child_idx(p_idx)
            self_len = len(self._elements)
            if r_idx < self_len:
                if self._method == 'min':
                    c = l_idx if self._elements[l_idx] < self._elements[r_idx] else r_idx
                else:
                    c = l_idx if self._elements[l_idx] > self._elements[r_idx] else r_idx
            elif r_idx >= self_len > l_idx:
                c = l_idx
            else:
                c = None
            return c

        if len(self._elements) > 1:
            child_idx = select_child(parent_idx)
            while not self.condition(parent_idx, child_idx):
                self.swap(child_idx, parent_idx)

                parent_idx = child_idx
                child_idx = select_child(parent_idx)
                if child_idx is None:
                    break

        return root

    def __len__(self):
        return len(self._elements)


if __name__ == '__main__':
    with open('data/prob7_data.txt', 'r') as f:
        data = f.read().split('\n')

    # data = [1,666,10,667,100,2,3]

    high_heap = Heap(method='min')
    low_heap = Heap(method='max')

    median = []

    for i, d in enumerate(data):
        d = int(d)

        high_heap_root = high_heap.root
        low_heap_root = low_heap.root

        if d > high_heap_root:
            high_heap.insert(d)
        elif d < low_heap_root:
            low_heap.insert(d)
        else:
            high_heap.insert(d)

        len_high = len(high_heap)
        len_low = len(low_heap)
        diff = len_low - len_high
        if abs(diff) > 1:
            if diff > 0:
                # max_heap has more elements
                tmp_element = low_heap.extract()
                high_heap.insert(tmp_element)
            else:
                # min_heap has more elements
                tmp_element = high_heap.extract()
                low_heap.insert(tmp_element)

        # get median
        len_high = len(high_heap)
        len_low = len(low_heap)
        if len_high > len_low:
            median.append(high_heap.root)
        elif len_high < len_low:
            median.append(low_heap.root)
        else:
            median.append(low_heap.root)

    print(sum(median))
    print(median)