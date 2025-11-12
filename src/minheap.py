class MinHeap:
    def __init__(self, key=None):
        self._a = []
        self._key = (lambda x: x) if key is None else key

    #public
    def __len__(self):
        return len(self._a)
    
    def is_empty(self):
        return len(self._a) == 0
    
    def peek(self):
        #returns smallest element, doesn't remove it
        if not self._a:
            raise IndexError("can't peek from empty heap")
        return self._a[0]

    def push(self, x):
        #insert x and restore heap property (sift-up)
        self._a.append(x)
        self._sift_up(len(self._a) - 1)

    def pop(self):
        #remove and return smallest element (soonest due date)
        if not self._a:
            raise IndexError("can't pop from empty heap")
        self._swap(0, len(self._a) - 1)
        x = self._a.pop()
        if self._a:
            self._sift_down(0)
        return x
    
    #private
    @staticmethod
    def _parent(i): return (i - 1) // 2

    @staticmethod
    def _left(i): return 2 * i + 1

    @staticmethod
    def _right(i): return 2 * i + 2

    def _less_index(self, i, j):
        #returns true if a[i] should come before a[j] based on key()
        return self._key(self._a[i]) < self._key(self._a[j])

    def _swap(self, i, j):
        self._a[i], self._a[j] = self._a[j], self._a[i]

    def _sift_up(self, i):
        while i > 0:
            parent_index = self._parent(i)
            if self._less_index(i, parent_index):
                self._swap(i, parent_index)
                i = parent_index
            else:
                break

    def _sift_down(self, i):
        heap_size = len(self._a)
        while True:
            left = self._left(i)
            right = self._right(i)
            smallest = i

            if left < heap_size and self._less_index(left, smallest):
                smallest = left
            if right < heap_size and self._less_index(right, smallest):
                smallest = right
            if smallest == i:
                break

            self._swap(i, smallest)
            i = smallest

    def heapify(self, arr):
        #builds heap in O(n) from an existing list
        self._a = list(arr)
        for i in range((len(self._a) - 2) // 2, -1, -1):
            self._sift_down(i)

    
