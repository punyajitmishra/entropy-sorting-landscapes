"""Count-only versions of the five algorithms with identical cost accounting
(comparisons C, writes M; a swap = 3 writes) to the instrumented originals."""
import sys
sys.setrecursionlimit(100000)

def bubble(a):
    a = list(a); n = len(a); C = M = 0
    for i in range(n - 1):
        sw = False
        for j in range(n - 1 - i):
            C += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]; M += 3; sw = True
        if not sw: break
    return C, M

def insertion(a):
    a = list(a); C = M = 0
    for i in range(1, len(a)):
        key = a[i]; j = i - 1
        while j >= 0:
            C += 1
            if a[j] <= key: break
            a[j + 1] = a[j]; M += 1; j -= 1
        a[j + 1] = key; M += 1
    return C, M

def merge(a):
    a = list(a); n = len(a); aux = [0] * n; cnt = [0, 0]
    def mrg(lo, mid, hi):
        for k in range(lo, hi + 1):
            aux[k] = a[k]; cnt[1] += 1
        i, j = lo, mid + 1
        for k in range(lo, hi + 1):
            if i > mid: a[k] = aux[j]; j += 1
            elif j > hi: a[k] = aux[i]; i += 1
            else:
                cnt[0] += 1
                if aux[i] <= aux[j]: a[k] = aux[i]; i += 1
                else: a[k] = aux[j]; j += 1
            cnt[1] += 1
    def srt(lo, hi):
        if lo >= hi: return
        mid = (lo + hi) // 2
        srt(lo, mid); srt(mid + 1, hi); mrg(lo, mid, hi)
    if a: srt(0, n - 1)
    return cnt[0], cnt[1]

def heap(a):
    a = list(a); n = len(a); cnt = [0, 0]
    def heapify(size, i):
        while True:
            lg = i; l = 2 * i + 1; r = 2 * i + 2
            if l < size:
                cnt[0] += 1
                if a[l] > a[lg]: lg = l
            if r < size:
                cnt[0] += 1
                if a[r] > a[lg]: lg = r
            if lg == i: return
            a[i], a[lg] = a[lg], a[i]; cnt[1] += 3; i = lg
    for i in range(n // 2 - 1, -1, -1): heapify(n, i)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]; cnt[1] += 3; heapify(end, 0)
    return cnt[0], cnt[1]

def quick(a):
    a = list(a); cnt = [0, 0]
    def part(lo, hi):
        piv = a[hi]; i = lo
        for j in range(lo, hi):
            cnt[0] += 1
            if a[j] <= piv:
                if i != j:
                    a[i], a[j] = a[j], a[i]; cnt[1] += 3
                i += 1
        if i != hi:
            a[i], a[hi] = a[hi], a[i]; cnt[1] += 3
        return i
    def srt(lo, hi):
        while lo < hi:
            p = part(lo, hi)
            srt(lo, p - 1); lo = p + 1
    if a: srt(0, len(a) - 1)
    return cnt[0], cnt[1]

ALG = {"bubble": bubble, "insertion": insertion, "merge": merge, "heap": heap, "quick": quick}

import random

def quick_rand(a, seed=0):
    a = list(a); cnt = [0, 0]; rnd = random.Random(seed)
    def part(lo, hi):
        p = rnd.randint(lo, hi)
        if p != hi:
            a[p], a[hi] = a[hi], a[p]; cnt[1] += 3
        piv = a[hi]; i = lo
        for j in range(lo, hi):
            cnt[0] += 1
            if a[j] <= piv:
                if i != j:
                    a[i], a[j] = a[j], a[i]; cnt[1] += 3
                i += 1
        if i != hi:
            a[i], a[hi] = a[hi], a[i]; cnt[1] += 3
        return i
    def srt(lo, hi):
        while lo < hi:
            p = part(lo, hi)
            if p - lo < hi - p:
                srt(lo, p - 1); lo = p + 1
            else:
                srt(p + 1, hi); hi = p - 1
    if a: srt(0, len(a) - 1)
    global LAST; LAST = a
    return cnt[0], cnt[1]

def quick_med3(a):
    a = list(a); cnt = [0, 0]
    def part(lo, hi):
        mid = (lo + hi) // 2
        if hi - lo >= 2:
            cnt[0] += 3
            x, y, z = a[lo], a[mid], a[hi]
            if (x <= y <= z) or (z <= y <= x): p = mid
            elif (y <= x <= z) or (z <= x <= y): p = lo
            else: p = hi
            if p != hi:
                a[p], a[hi] = a[hi], a[p]; cnt[1] += 3
        piv = a[hi]; i = lo
        for j in range(lo, hi):
            cnt[0] += 1
            if a[j] <= piv:
                if i != j:
                    a[i], a[j] = a[j], a[i]; cnt[1] += 3
                i += 1
        if i != hi:
            a[i], a[hi] = a[hi], a[i]; cnt[1] += 3
        return i
    def srt(lo, hi):
        while lo < hi:
            p = part(lo, hi)
            if p - lo < hi - p:
                srt(lo, p - 1); lo = p + 1
            else:
                srt(p + 1, hi); hi = p - 1
    if a: srt(0, len(a) - 1)
    global LAST; LAST = a
    return cnt[0], cnt[1]

def natural_merge(a):
    """Bottom-up merge of maximal non-decreasing runs. Run detection costs n-1
    comparisons; merges use the same accounting as merge_sort."""
    a = list(a); n = len(a)
    if n < 2: return 0, 0
    C = M = 0
    runs = []; s = 0
    for i in range(1, n):
        C += 1
        if a[i - 1] > a[i]:
            runs.append((s, i - 1)); s = i
    runs.append((s, n - 1))
    aux = [0] * n
    while len(runs) > 1:
        new = []
        for k in range(0, len(runs) - 1, 2):
            lo, mid = runs[k]; mid = runs[k][1]; hi = runs[k + 1][1]; lo = runs[k][0]
            for t in range(lo, hi + 1):
                aux[t] = a[t]; M += 1
            i, j = lo, mid + 1
            for t in range(lo, hi + 1):
                if i > mid: a[t] = aux[j]; j += 1
                elif j > hi: a[t] = aux[i]; i += 1
                else:
                    C += 1
                    if aux[i] <= aux[j]: a[t] = aux[i]; i += 1
                    else: a[t] = aux[j]; j += 1
                M += 1
            new.append((lo, hi))
        if len(runs) % 2: new.append(runs[-1])
        runs = new
    global LAST; LAST = a
    return C, M

def run_entropy(a):
    """Run-based entropy H(A) (Gila et al.-style) using maximal ascending runs, natural log-base 2."""
    import math
    n = len(a); r = []; s = 0
    for i in range(1, n):
        if a[i - 1] > a[i]: r.append(i - s); s = i
    r.append(n - s)
    return sum(x / n * math.log2(n / x) for x in r)
