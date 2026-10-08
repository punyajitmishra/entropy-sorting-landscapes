import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 8, "font.family": "serif", "axes.linewidth": 0.6, "lines.linewidth": 1.1,
                     "legend.fontsize": 7, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7})
style = {"bubble": ("Bubble", "#7f7f7f", "-"), "insertion": ("Insertion", "#1f77b4", "--"), "merge": ("Merge", "#2ca02c", "-"),
         "heap": ("Heap", "#d62728", "-"), "quick": ("Quick (last pivot)", "#ff7f0e", "-."),
         "quick_rand": ("Quick (random pivot)", "#ff7f0e", ":"), "natural_merge": ("Natural merge", "#2ca02c", ":")}
# ---- Figure 1: trajectories
d = np.load("results/traj.npz"); g = d["grid"]
fig, ax = plt.subplots(1, 2, figsize=(7.16, 2.55))
for k in ["bubble", "insertion", "merge", "heap", "quick"]:
    lab, c, ls = style[k]; E = d["E_" + k]; S = d["S_" + k]
    ax[0].plot(g, E.mean(0), color=c, ls=ls, label=lab)
    ax[1].plot(g, (S / S[:, [0]]).mean(0), color=c, ls=ls, label=lab)
ax[0].set_xlabel("fraction of recorded states"); ax[0].set_ylabel(r"disorder energy $E_t=m_t/m_{\max}$"); ax[0].set_title("(a)", fontsize=8, loc="left")
ax[1].set_xlabel("fraction of recorded states"); ax[1].set_ylabel(r"$S(m_t)/S(m_0)$"); ax[1].set_title("(b)", fontsize=8, loc="left")
ax[0].legend(frameon=False, loc="lower left"); 
for a in ax: a.grid(alpha=0.25, lw=0.4)
fig.tight_layout(); fig.savefig("fig/trajectories.pdf"); plt.close(fig)
# ---- Figure 2: W vs n
sweep = json.load(open("results/sweep.json"))
fig, ax = plt.subplots(1, 2, figsize=(7.16, 2.7))
for j, (dist, title) in enumerate([("uniform_random", "(a) uniform-random"), ("nearly_sorted", "(b) nearly-sorted")]):
    for k in ["bubble", "insertion", "merge", "heap", "quick", "quick_rand", "natural_merge"]:
        lab, c, ls = style[k]; ns = []; ws = []
        for b in sweep:
            if b["dist"] == dist:
                ns.append(b["n"]); ws.append(np.mean(np.array(b[k]["C"]) + np.array(b[k]["M"])))
        ax[j].loglog(ns, ws, color=c, ls=ls, marker="o", ms=2.2, label=lab)
    ax[j].set_xlabel("array size $n$"); ax[j].set_ylabel("mean operation cost $W=C+M$"); ax[j].set_title(title, fontsize=8, loc="left"); ax[j].grid(alpha=0.25, lw=0.4, which="both")
ax[0].axvline(23, color="k", lw=0.5, ls=":"); ax[0].text(24.5, 75, r"$n^\ast\!\approx\!23$", fontsize=6.5)
ax[0].legend(frameon=False, loc="upper left")
fig.tight_layout(); fig.savefig("fig/cost_vs_n.pdf"); plt.close(fig)
print("figs ok")
