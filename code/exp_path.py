import json, numpy as np
from algorithms import ALGORITHMS, Tracker
from states import exact_log_omega, max_inv
Tracker.VALIDATE = False
n = 100; S = exact_log_omega(n); res = {}
rng = np.random.default_rng(np.random.SeedSequence(entropy=20260927, spawn_key=(4, 1)))
arrs = [rng.permutation(n) for _ in range(30)]           # same 30 inputs as exp_traj
for name, f in ALGORITHMS.items():
    lam = []; net = []
    for a in arrs:
        s, t = f(a); m = np.array(t.inversions); Sm = S[m]
        lam.append(np.abs(np.diff(Sm)).sum() / Sm[0]); net.append(Sm[0])
    res[name] = {"path_over_net": float(np.mean(lam)), "sd": float(np.std(lam)), "S0": float(np.mean(net))}
    print(name, res[name])
ill = json.load(open("results/traj.json"))["illustrative"]
print({k: (v["C"], v["M"], v["W"], v["steps"]) for k, v in ill.items() if isinstance(v, dict)})
print({k: ill[k] for k in ("S17_exact","S17_gauss","S_peak_exact","S_peak_gauss","peak_m")})
json.dump(res, open("results/path.json", "w"))
