import json, numpy as np, math
from states import exact_log_omega, gaussian_log_omega, max_inv
main = json.load(open("results/main.json")); sweep = json.load(open("results/sweep.json")); fine = json.load(open("results/fine.json"))
ALGS = ["bubble","insertion","merge","heap","quick","quick_med3","quick_rand","natural_merge"]
print("=== MAIN n=100, N=1000 (reverse: 1) ===")
for blk in main:
    d = blk["dist"]; E0 = np.array(blk["E0"]) if blk["E0"] else None
    print("\n", d, "trials", blk["trials"], "H mean %.3f" % np.mean(blk["H"]), ("E0 %.3f +- %.3f" % (E0.mean(), E0.std())) if E0 is not None else "")
    for a in ALGS:
        C = np.array(blk[a]["C"]); M = np.array(blk[a]["M"]); W = C + M
        s = "%-13s C=%8.1f M=%8.1f W=%8.1f +- %6.1f" % (a, C.mean(), M.mean(), W.mean(), W.std())
        if E0 is not None:
            R = E0 / W * 1e4; s += "  R=%6.3f +- %5.3f" % (R.mean(), R.std())
        print(s)
    if E0 is not None and d != "reverse_sorted":
        # per-trial rank consistency: is R ranking the exact inverse of W ranking within each distribution?
        Ws = np.array([[np.array(blk[a]["C"])[i] + np.array(blk[a]["M"])[i] for a in ALGS[:5]] for i in range(blk["trials"])])
        print("  mean-R order:", sorted(ALGS[:5], key=lambda a: -np.mean(E0 / (np.array(blk[a]["C"]) + np.array(blk[a]["M"])))))
        print("  mean-W order:", sorted(ALGS[:5], key=lambda a: np.mean(np.array(blk[a]["C"]) + np.array(blk[a]["M"]))))
# ranking of the original five by mean W per distribution, plus rank of Heap etc
print("\n=== SWEEP mean W (uniform / nearly / reverse / few) ===")
for blk in sweep:
    print(blk["n"], blk["dist"][:7], blk["trials"], " ".join("%s=%.0f" % (a[:6], np.mean(np.array(blk[a]["C"]) + np.array(blk[a]["M"]))) for a in ALGS))
print("\n=== FINE crossover insertion vs merge (uniform) ===")
prev = None
for blk in fine:
    n = blk["n"]; wi = np.mean(np.array(blk["insertion"]["C"]) + np.array(blk["insertion"]["M"])); wm = np.mean(np.array(blk["merge"]["C"]) + np.array(blk["merge"]["M"]))
    wq = np.mean(np.array(blk["quick"]["C"]) + np.array(blk["quick"]["M"])); wh = np.mean(np.array(blk["heap"]["C"]) + np.array(blk["heap"]["M"]))
    if n % 5 == 0 or (prev is not None and (wi > wm) != prev): print(n, "W_ins=%.1f W_merge=%.1f W_quick=%.1f W_heap=%.1f  ins>merge=%s ins>quick=%s ins>heap=%s" % (wi, wm, wq, wh, wi > wm, wi > wq, wi > wh))
    prev = wi > wm
# theory: exact merge writes and average insertion cost
def mw(n, memo={}):
    if n <= 1: return 0
    if n in memo: return memo[n]
    memo[n] = mw((n + 1) // 2) + mw(n // 2) + 2 * n; return memo[n]
print("exact merge writes M(n):", {n: mw(n) for n in (10, 27, 28, 100)})
H = lambda n: sum(1 / k for k in range(1, n + 1))
print("E[W_ins](n) = n(n-1)/2 + 2(n-1) - (H_n - 1):", {n: round(n*(n-1)/2 + 2*(n-1) - (H(n)-1), 2) for n in (10, 27, 28, 30, 100)})
print("\n=== Gaussian vs exact entropy, n=100 ===")
S = exact_log_omega(100); G = gaussian_log_omega(100); mm = max_inv(100)
for E in (0.5, 0.3, 0.1, 0.05, 0.01):
    m = int(round(E * mm)); print("E=%.2f m=%d exact=%.2f gauss=%.2f diff=%.2f" % (E, m, S[m], G[m], G[m] - S[m]))
print("peak exact %.3f (m=%d)  gauss %.3f  ln 100! = %.3f" % (S.max(), S.argmax(), G.max(), math.lgamma(101)))
S10 = exact_log_omega(10); G10 = gaussian_log_omega(10); print("n=10 m=5: exact %.3f gauss %.3f; m=1: exact %.3f gauss %.3f" % (S10[5], G10[5], S10[1], G10[1]))
print("Var check n=100 uniform E0 sd (theory) ", math.sqrt(100*99*205/72)/4950)
