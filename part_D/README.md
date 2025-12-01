## Part D: Exact vs Approximation Plots

This folder contains scripts and outputs for **Part D**, where you:

- Plot **runtime (wall clock)** of the exact solution vs the approximation on your test cases.
- Plot **solution quality** (path length) of the exact vs the approximation on the same test cases.

The project already has comparison + data-generation scripts at the project root; Part D reuses those and adds plots saved into this folder.

---

### 1. Generate comparison data (from project root)

From the project root (`NP-Complete-Project-`), run:

```bash
bash compare_solutions_detailed.sh
```

This:
- Runs **exact** (`exact_solution/cs412_longestpath_exact.py`) and **approx** (`approx_solution/cs412_longestpath_approx.py`) on the common test cases in `approx_solution/test_cases/`.
- Measures **wall-clock runtime** for each.
- Records the **optimal path length** vs the **approximate path length**.
- Writes results to:
  - `comparison_data.txt` (raw data used for plotting)
  - `comparison_summary.txt` (text summary)

Make sure this command finishes successfully before plotting.

---

### 2. Generate Part D plots into this folder

From the project root, run:

```bash
python3 part_D/plot_part_D.py
```

This script:

- Reads `comparison_data.txt` from the project root.
- Produces two sets of plots in `part_D/`:
  - `part_D_runtime_comparison.png` / `.pdf`  
    **Runtime (seconds, log scale)** vs **number of vertices**, comparing exact vs approximation.
  - `part_D_solution_quality.png` / `.pdf`  
    **Path length** (objective value) vs **number of vertices**, comparing exact vs approximation.

These two plots are exactly what you need for:

- **Runtime comparison** (wall-clock performance).
- **Solution-quality comparison** (how close the approximation is to optimal).

---

### 3. Optional: Existing combined comparison plot

There is also an existing script at the project root:

```bash
python3 plot_comparison.py
```

It reads the same `comparison_data.txt` and generates a more detailed multi-panel figure:
- Runtime comparison (log scale)
- Solution value comparison
- Speedup bar chart
- Quality table

That figure is saved as:

- `solution_comparison.png`
- `solution_comparison.pdf`

You can reference those as additional visuals, but **Part D’s required plots are the ones written into this `part_D` folder.**



