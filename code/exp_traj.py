import json, numpy as np
from algorithms import ALGORITHMS, Tracker
from states import inversion_count, max_inv, exact_log_omega, gaussian_log_omega

# ---- (a) illustrative n=10 trial: first seeded uniform permutation with m0 = 17
rng = np.random.default_rng(np.random.SeedSequence(entropy=20260927, spawn_key=(4, 0)))
while True:
    a = rng.permutation(10)
    if inversion_count(a) == 17: break
Tracker.VALIDATE = True
ill = {"input": a.tolist()}
S10 = exact_log_omega(10)
for name, f in ALGORITHMS.items():
    s, t = f(a)
    assert list(s) == sorted(a.tolist())
    C, M = t.comparisons, t.write_ops
    ill[name] = {"traj": t.inversions, "C": C, "M": M, "W": C + M, "steps": len(t.inversions) - 1}
ill["S17_exact"] = float(S10[17]); ill["S_peak_exact"] = float(S10.max()); ill["peak_m"] = int(S10.argmax())
g = gaussian_log_omega(10); ill["S_peak_gauss"] = float(g.max()); ill["S17_gauss"] = float(g[17])

# ---- (b) n=100 trajectories, uniform random, 30 trials, exact entropy
Tracker.VALIDATE = False
n = 100; mm = max_inv(n); S = exact_log_omega(n)
stats = {}; grid = np.linspace(0, 1, 101); curves = {k: [] for k in ALGORITHMS}; scurves = {k: [] for k in ALGORITHMS}
rng = np.random.default_rng(np.random.SeedSequence(entropy=20260927, spawn_key=(4, 1)))
arrs = [rng.permutation(n) for _ in range(30)]
for name, f in ALGORITHMS.items():
    inc = []; exc = []; maxdrop = []; steps = []; peakE = []
    for a in arrs:
        s, t = f(a); m = np.array(t.inversions); assert (np.diff(np.sort(s)) >= 0).all() and (s[:-1] <= s[1:]).all()
        d = np.diff(m); m0 = m[0]
        steps.append(len(m) - 1); inc.append(float((d > 0).mean())); exc.append((m.max() - m0) / mm)
        maxdrop.append(float(-d.min() / m0)); peakE.append(m.max() / mm)
        x = np.linspace(0, 1, len(m)); curves[name].append(np.interp(grid, x, m / mm)); scurves[name].append(np.interp(grid, x, S[m]))
    stats[name] = {"steps": float(np.mean(steps)), "frac_increase": float(np.mean(inc)), "max_excursion_E": float(np.mean(exc)),
                   "max_single_drop_frac_m0": float(np.mean(maxdrop)), "peak_E": float(np.mean(peakE))}
np.savez("results/traj.npz", grid=grid, **{f"E_{k}": np.array(v) for k, v in curves.items()}, **{f"S_{k}": np.array(v) for k, v in scurves.items()})
json.dump({"illustrative": ill, "stats": stats, "S100_peak": float(S.max()), "S100_peak_m": int(S.argmax())}, open("results/traj.json", "w"), indent=1)
print(json.dumps(stats, indent=1)); print(ill["input"], {k: (v["traj"] if k in ALGORITHMS else v) for k, v in ill.items() if k in ALGORITHMS})
