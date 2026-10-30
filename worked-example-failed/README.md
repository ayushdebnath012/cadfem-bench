# Worked example 2: a failed run (BT-plate-08, GPT-6 Astra)

Files behind https://ayushdebnath012.github.io/cadfem-bench/worked-example-failed.html

| File | What it is |
|---|---|
| `astra-main.py` | The program GPT-6 Astra returned (one call, no tools, no feedback), unchanged |
| `astra-solver.log`, `astra-results.json`, `astra-refinement.json` | Its outputs from one offline sandbox run (26 s, exit 0) |
| `astra-score.json` | `score.py` verdict: lambda1 = 0.8701 vs reference 0.379, error +129.6 %, numbers fail |
| `fix.diff` | The only change we made: each buckling run repeated at 10 % of the load, factors scaled back; hand estimate logged |
| `fixed-main.py` | Astra's program with that change |
| `fixed-solver.log`, `fixed-results.json`, `fixed-refinement.json` | Outputs from the same sandbox (31.5 s, exit 0) |
| `fixed-score.json` | `score.py` verdict: lambda1 = 0.37903, error +0.008 %, numbers pass |

Both runs used the buckle-trap package (`buckle-traps-0.1`), CalculiX 2.23, the macOS sandbox (no network, 600 s, 6 GB).
Both score files also list `part.step`, `mesh.msh`, `fields.npz` and `environment.json` as missing: the scorer checks the
main-task file list, while this trap task asks only for `results.json`, `main.py` and `solver.log`. This is a known scorer
issue and changes neither verdict. Neither run has had the expert human annotator review.

The fix was written by us after the run, knowing the answer. It shows the failure comes from one missing check; it does
not show Astra would have found it. 10 % suits this plate; a general program should lower the load until the smallest
factor stops changing, or count modes below its answer (Sturm count, see case-study.html).
