from collections import Counter
from states import inversion_count

class Tracker:
    VALIDATE = True
    def __init__(self, initial):
        self.initial = initial.copy(); self.inversions = []
        self.comparisons = 0; self.swaps = 0; self.write_ops = 0
        self.record_state(initial)
    def record_state(self, a):
        snap = a.copy()
        if Tracker.VALIDATE and Counter(snap.tolist() if hasattr(snap,'tolist') else snap) != Counter(self.initial.tolist() if hasattr(self.initial,'tolist') else self.initial):
            raise ValueError("State is not a permutation of the initial input.")
        self.inversions.append(inversion_count(snap))
    def compare(self): self.comparisons += 1
    def swap(self, a, i, j):
        self.swaps += 1; self.write_ops += 3
        a[i], a[j] = a[j], a[i]; self.record_state(a)

def bubble_sort(arr):
    a = arr.copy(); t = Tracker(a); n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            t.compare()
            if a[j] > a[j + 1]:
                t.swap(a, j, j + 1); swapped = True
        if not swapped: break
    return a, t

def insertion_sort(arr):
    a = arr.copy(); t = Tracker(a)
    for i in range(1, len(a)):
        key = a[i]; j = i - 1
        while j >= 0:
            t.compare()
            if a[j] <= key: break
            a[j + 1] = a[j]; t.write_ops += 1; j -= 1
        a[j + 1] = key; t.write_ops += 1; t.record_state(a)
    return a, t

def merge_sort(arr):
    a = arr.copy(); t = Tracker(a); aux = [0] * len(a)
    def merge(lo, mid, hi):
        for k in range(lo, hi + 1):
            aux[k] = a[k]; t.write_ops += 1
        i, j = lo, mid + 1
        for k in range(lo, hi + 1):
            if i > mid: a[k] = aux[j]; j += 1
            elif j > hi: a[k] = aux[i]; i += 1
            else:
                t.compare()
                if aux[i] <= aux[j]: a[k] = aux[i]; i += 1
                else: a[k] = aux[j]; j += 1
            t.write_ops += 1
        t.record_state(a)
    def sort(lo, hi):
        if lo >= hi: return
        mid = (lo + hi) // 2
        sort(lo, mid); sort(mid + 1, hi); merge(lo, mid, hi)
    if len(a): sort(0, len(a) - 1)
    return a, t

def heap_sort(arr):
    a = arr.copy(); t = Tracker(a); n = len(a)
    def heapify(size, i):
        while True:
            largest = i; l = 2*i+1; r = 2*i+2
            if l < size:
                t.compare()
                if a[l] > a[largest]: largest = l
            if r < size:
                t.compare()
                if a[r] > a[largest]: largest = r
            if largest == i: return
            t.swap(a, i, largest); i = largest
    for i in range(n // 2 - 1, -1, -1): heapify(n, i)
    for end in range(n - 1, 0, -1):
        t.swap(a, 0, end); heapify(end, 0)
    return a, t

def quick_sort(arr):
    a = arr.copy(); t = Tracker(a)
    def partition(lo, hi):
        pivot = a[hi]; i = lo
        for j in range(lo, hi):
            t.compare()
            if a[j] <= pivot:
                if i != j: t.swap(a, i, j)
                i += 1
        if i != hi: t.swap(a, i, hi)
        return i
    def sort(lo, hi):
        if lo >= hi: return
        p = partition(lo, hi); sort(lo, p - 1); sort(p + 1, hi)
    if len(a): sort(0, len(a) - 1)
    return a, t

ALGORITHMS = {"bubble": bubble_sort, "insertion": insertion_sort, "merge": merge_sort,
              "heap": heap_sort, "quick": quick_sort}
