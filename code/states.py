import numpy as np, math
from math import lgamma

def inversion_count(arr):
    a = np.asarray(arr); n = len(a)
    if n < 2: return 0
    ranks = np.empty(n, dtype=int); ranks[np.argsort(a, kind="stable")] = np.arange(n)
    bit = np.zeros(n + 1, dtype=int); total = 0
    for r in ranks:
        k = r + 1; s = 0
        while k: s += bit[k]; k -= k & -k
        total += r - s; k = r + 1
        while k <= n: bit[k] += 1; k += k & -k
    return int(total)

def max_inv(n): return n * (n - 1) // 2

def exact_omega_int(n):
    """Exact Mahonian numbers Omega_n(m), m=0..n(n-1)/2, as Python integers
    (coefficients of prod_{k=1}^n (1+q+...+q^{k-1}))."""
    from itertools import accumulate
    mm = max_inv(n); c = [1] + [0] * mm
    for k in range(2, n + 1):
        P = [0] + list(accumulate(c))
        c = [P[m + 1] - P[max(0, m - k + 1)] for m in range(mm + 1)]
    return c

_LOGCACHE = {}
def exact_log_omega(n):
    """ln Omega_n(m) computed from exact integers (no floating-point underflow/cancellation)."""
    if n not in _LOGCACHE:
        _LOGCACHE[n] = np.array([math.log(x) for x in exact_omega_int(n)])
    return _LOGCACHE[n]

def gaussian_log_omega(n):
    mm = max_inv(n); m = np.arange(mm + 1, dtype=float)
    mu = n*(n-1)/4; var = n*(n-1)*(2*n+5)/72
    h = lgamma(n + 1) - 0.5*np.log(2*np.pi*var) - (m-mu)**2/(2*var)
    h[0] = 0.0; h[-1] = 0.0
    return h
