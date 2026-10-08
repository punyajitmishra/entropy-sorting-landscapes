import json, numpy as np
from scipy.special import logsumexp
from algorithms import ALGORITHMS, Tracker
from states import exact_log_omega, max_inv

n = 100; mm = max_inv(n); S = exact_log_omega(n); m = np.arange(mm + 1); E = m / mm
# effective inverse temperature beta_eff(m) = dS/dE (central difference), defined for 0<m<mmax
beta_eff = np.full(mm + 1, np.nan); beta_eff[1:-1] = mm * (S[2:] - S[:-2]) / 2
# ---- exact canonical ensemble at n=100
out = {"ensemble": []}
for beta in [-20, -10, 0, 10, 20, 50, 100, 200, 400]:
    lw = S - beta * E; lZ = logsumexp(lw); p = np.exp(lw - lZ)
    Em = (p * E).sum(); sd = np.sqrt((p * E**2).sum() - Em**2); mode = int(np.argmax(p))
    F = -lZ / beta if beta != 0 else None
    out["ensemble"].append({"beta": beta, "E_mean": float(Em), "E_sd": float(sd), "mode_m": mode,
                            "beta_eff_at_mode": float(beta_eff[mode]) if 0 < mode < mm else None,
                            "lnZ": float(lZ), "F": F, "cv": float(beta**2 * sd**2)})
    print(out["ensemble"][-1])
# ---- effective temperature along trajectories (same 30 uniform-random inputs as exp_traj/exp_path)
Tracker.VALIDATE = False
rng = np.random.default_rng(np.random.SeedSequence(entropy=20260927, spawn_key=(4, 1)))
arrs = [rng.permutation(n) for _ in range(30)]
grid = np.linspace(0, 1, 101); curves = {}; stats = {}
for name, f in ALGORITHMS.items():
    neg = []; bmin = []; b0 = []; frac_mid = []; cs = []
    for a in arrs:
        s, t = f(a); mm_t = np.array(t.inversions); interior = (mm_t > 0) & (mm_t < mm); b = beta_eff[mm_t[interior]]
        neg.append(float((b < 0).mean())); bmin.append(float(np.nanmin(b))); b0.append(float(beta_eff[mm_t[0]]) if 0 < mm_t[0] < mm else np.nan)
        x = np.linspace(0, 1, len(mm_t)); cs.append(np.interp(grid, x, np.nan_to_num(beta_eff[mm_t], nan=beta_eff[mm_t[mm_t > 0].min()] if False else 0)))
    curves[name] = np.array(cs)
    stats[name] = {"frac_negative_beta": float(np.mean(neg)), "min_beta_mean": float(np.mean(bmin)), "min_beta_min": float(np.min(bmin)), "beta0_mean": float(np.nanmean(b0))}
    print(name, stats[name])
out["traj_beta"] = stats; out["beta_eff_at"] = {str(int(mm * e)): float(beta_eff[int(mm * e)]) for e in (0.5, 0.3, 0.1, 0.05, 0.01)}
json.dump(out, open("results/ensemble.json", "w"), indent=1)
np.savez("results/beta_curves.npz", grid=grid, **{f"b_{k}": v for k, v in curves.items()})
print(out["beta_eff_at"])
