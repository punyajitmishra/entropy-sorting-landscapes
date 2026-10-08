import json, time, sys
import numpy as np
import fastcount as fc
from states import inversion_count, max_inv

ALGS = {"bubble": fc.bubble, "insertion": fc.insertion, "merge": fc.merge, "heap": fc.heap,
        "quick": fc.quick, "quick_med3": fc.quick_med3, "natural_merge": fc.natural_merge}
DISTS = ["uniform_random", "nearly_sorted", "reverse_sorted", "few_unique"]
SS = np.random.SeedSequence(20260927)

def gen(n, dist, rng):
    if dist == "uniform_random": return rng.permutation(n)
    if dist == "nearly_sorted":
        a = np.arange(n)
        for _ in range(max(1, int(0.05 * n))):
            i, j = rng.integers(0, n, 2); a[i], a[j] = a[j], a[i]
        return a
    if dist == "reverse_sorted": return np.arange(n - 1, -1, -1)
    return rng.integers(0, 5, size=n)

def run(n, dist, trials, seed_key):
    rng = np.random.default_rng(np.random.SeedSequence(entropy=20260927, spawn_key=seed_key))
    if dist == "reverse_sorted": trials = 1
    arrs = [gen(n, dist, rng) for _ in range(trials)]
    out = {"n": n, "dist": dist, "trials": trials}
    mm = max_inv(n)
    out["E0"] = [inversion_count(a) / mm for a in arrs] if dist != "few_unique" else None
    out["H"] = [fc.run_entropy(a.tolist()) for a in arrs]
    algs = dict(ALGS)
    for name, f in algs.items():
        CM = [f(a.tolist()) for a in arrs]
        out[name] = {"C": [c for c, m in CM], "M": [m for c, m in CM]}
    # randomized-pivot Quick Sort: independent per-trial seeds
    CM = [fc.quick_rand(a.tolist(), seed=int(rng.integers(1 << 31))) for a in arrs]
    out["quick_rand"] = {"C": [c for c, m in CM], "M": [m for c, m in CM]}
    return out

mode = sys.argv[1]
t0 = time.time()
if mode == "main":
    res = [run(100, d, 1000, (1, k)) for k, d in enumerate(DISTS)]
    json.dump(res, open("results/main.json", "w"))
elif mode == "sweep":
    res = []
    for ni, n in enumerate([10, 20, 50, 100, 200, 500, 1000, 2000]):
        tr = 100 if n <= 500 else 30
        for k, d in enumerate(DISTS):
            res.append(run(n, d, tr, (2, ni, k))); print("sweep", n, d, round(time.time() - t0), flush=True)
    json.dump(res, open("results/sweep.json", "w"))
elif mode == "fine":
    res = []
    for n in range(10, 61):
        res.append(run(n, "uniform_random", 400, (3, n)))
    json.dump(res, open("results/fine.json", "w"))
print("done", mode, round(time.time() - t0), "s")
