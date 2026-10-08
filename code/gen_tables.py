import json, numpy as np
main = json.load(open("results/main.json")); sweep = json.load(open("results/sweep.json"))
traj = json.load(open("results/traj.json")); path = json.load(open("results/path.json"))
NAME = {"bubble": "Bubble", "insertion": "Insertion", "merge": "Merge", "heap": "Heap", "quick": "Quick (last pivot)",
        "quick_med3": "Quick (median-of-3)", "quick_rand": "Quick (random pivot)", "natural_merge": "Natural merge"}
ORDER = ["bubble", "insertion", "merge", "heap", "quick", "quick_med3", "quick_rand", "natural_merge"]
def th(x, d=0):  # thousands with braces-comma for math mode
    return f"{x:,.{d}f}".replace(",", "{,}")
B = {b["dist"]: b for b in main}
def WR(dist, a, dagger=False):
    b = B[dist]; W = np.array(b[a]["C"]) + np.array(b[a]["M"]); w = W.mean(); sw = W.std()
    if b["trials"] == 1: ws = f"${th(w)}" + (r"^\dagger" if dagger else "") + "$"
    else: ws = f"${th(w, 1 if w < 100000 else 0)}\\pm{sw:,.1f}$".replace(",", "{,}") if False else f"${th(w)}\\pm{sw:.1f}$"
    if b["E0"] is None: return ws, None
    E0 = np.array(b["E0"]); R = E0 / W * 1e4
    rs = f"${R.mean():.3f}$" if b["trials"] == 1 else f"${R.mean():.3f}\\pm{R.std():.3f}$"
    return ws, rs
rows = []
for a in ORDER:
    u = WR("uniform_random", a); n_ = WR("nearly_sorted", a); r = WR("reverse_sorted", a, dagger=(a == "quick_rand")); f = WR("few_unique", a)
    rows.append(f"{NAME[a]} & {u[0]} & {u[1]} & {n_[0]} & {n_[1]} & {r[0]} & {r[1]} & {f[0]} \\\\")
    if a == "quick": pass
cost = "\n".join(rows)
# sweep table (uniform W means)
ns = [10, 20, 50, 100, 200, 500, 1000, 2000]
S = {(b["n"], b["dist"]): b for b in sweep}
srows = []
for a in ORDER:
    cells = []
    for n in ns:
        b = S[(n, "uniform_random")]; cells.append("$" + th(np.mean(np.array(b[a]["C"]) + np.array(b[a]["M"]))) + "$")
    srows.append(f"{NAME[a]} & " + " & ".join(cells) + " \\\\")
sw = "\n".join(srows)
# nearly-sorted sweep table
nrows = []
for a in ORDER:
    cells = []
    for n in ns:
        b = S[(n, "nearly_sorted")]; cells.append("$" + th(np.mean(np.array(b[a]["C"]) + np.array(b[a]["M"]))) + "$")
    nrows.append(f"{NAME[a]} & " + " & ".join(cells) + " \\\\")
sn = "\n".join(nrows)
# trajectory table
st = traj["stats"]; trows = []
for a in ["bubble", "insertion", "merge", "heap", "quick"]:
    s = st[a]; p = path[a]
    trows.append(f"{NAME[a]} & ${s['steps']:.1f}$ & ${100*s['frac_increase']:.1f}$ & ${s['peak_E']:.3f}$ & ${100*s['max_single_drop_frac_m0']:.2f}$ & ${p['path_over_net']:.3f}$ \\\\")
tr = "\n".join(trows)
# illustrative trial
ill = traj["illustrative"]; irows = []
for a in ["bubble", "insertion", "merge", "heap", "quick"]:
    v = ill[a]; t = "$" + "\\!\\to\\!".join(str(x) for x in v["traj"]) + "$"
    irows.append(f"{NAME[a]} & {v['C']} & {v['M']} & {v['W']} & {v['steps']} & {t} \\\\")
il = "\n".join(irows)
json.dump({"cost": cost, "sweep": sw, "sweepn": sn, "traj": tr, "ill": il}, open("results/tables.json", "w"), indent=1)
print(cost); print(); print(sw); print(); print(tr); print(); print(il[:300])
