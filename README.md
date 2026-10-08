# Entropy Landscapes and Kinetics of Classical Sorting Algorithms

Supplementary code, results and paper source for *"Entropy Landscapes and Kinetics of
Classical Sorting Algorithms"* (Punyajit Mishra, 2026).

The paper treats a permutation as a microstate and its inversion count as a macrostate,
computes the exact entropy landscape from the Mahonian distribution, and tracks how Bubble,
Insertion, Merge, Heap and Quick Sort move through it (plus an effective inverse temperature
read off the exact landscape).

## Layout

    code/      Python source, results/ (exact outputs used in the paper), fig/ (generated figures)
    paper/     paper.tex (IEEEtran), fig/ (copies of the two figures), paper.pdf (compiled)

## Setup

Python 3.12. Dependencies are in `requirements.txt` (NumPy, SciPy, Matplotlib).

    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt

## Reproducing the results

Run from inside `code/`:

    python exp_main.py main        # n=100, 1000 trials/distribution -> results/main.json
    python exp_main.py fine        # n=10..60 crossover sweep        -> results/fine.json
    python exp_main.py sweep       # n=10..2000                      -> results/sweep.json
    python exp_traj.py             # instrumented trajectories       -> results/traj.json, traj.npz
    python exp_path.py             # entropy path length Lambda      -> results/path.json
    python exp_ensemble.py         # exact canonical ensemble + beta_eff -> results/ensemble.json, beta_curves.npz
    python gen_tables.py           # LaTeX table bodies              -> results/tables.json
    python figs.py                 # figures                         -> fig/
    python analyze.py              # console summary of every number quoted in the paper

The whole pipeline takes a few minutes on one CPU core. All random streams derive from
`numpy.random.SeedSequence(entropy=20260927)` with distinct spawn keys, so results do not
depend on execution order. `results/` holds the exact outputs used in the paper, so you can
skip straight to `figs.py` / `analyze.py`.

## Files

| File | Purpose |
|---|---|
| `states.py` | Exact Mahonian counts with Python big integers (validated by brute force for n=5,6,7; sum = n! and symmetry at n=100) |
| `algorithms.py` | Instrumented sorts that record (comparisons, writes, state) |
| `fastcount.py` | Count-only sorts with identical cost accounting (validated on 20 arrays, 4 distributions, 5 algorithms) |
| `exp_*.py` | Experiments |
| `gen_tables.py`, `figs.py`, `analyze.py` | Tables, figures, console summary |

## Building the paper

`paper/paper.tex` uses the IEEEtran class (TeX Live package `texlive-publishers`) and
`placeins`. The table bodies in the paper were typeset by hand from the values in
`code/results/`; `gen_tables.py` emits the same numbers as LaTeX if you want to regenerate them.

    cd paper && pdflatex paper.tex && pdflatex paper.tex

## Citation

See `CITATION.cff`. Licensed under the MIT License.
