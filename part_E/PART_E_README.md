# Part E: Comprehensive Test Case Comparison

This directory contains scripts and results for generating 1000+ test cases and performing a comprehensive comparison between the exact (optimal) and approximation solutions for the Longest Path problem.

## Files

- `generate_test_cases.py` - Generates 1000+ diverse test cases
- `run_comparison.py` - Runs both solutions on all test cases
- `analyze_comparison.py` - Analyzes results and generates comprehensive report
- `run_part_e.sh` - Master script that runs all steps in sequence
- `part_e_test_cases/` - Directory containing generated test cases
- `part_e_comparison_results.json` - Raw comparison results (JSON)
- `part_e_comparison_report.txt` - Comprehensive analysis report

## Quick Start

To run the complete analysis:

```bash
chmod +x run_part_e.sh
./run_part_e.sh
```

Or run steps individually:

```bash
# Step 1: Generate test cases
python3 generate_test_cases.py

# Step 2: Run comparison (may take a while)
python3 run_comparison.py

# Step 3: Analyze results
python3 analyze_comparison.py
```

## Test Case Types

The generator creates diverse test cases including:

1. **Small graphs (3-5 vertices)** - 300 cases
   - Complete graphs
   - Trees
   - Paths
   - Cycles
   - Sparse graphs
   - Dense graphs
   - Greedy trap graphs (designed to fool greedy algorithms)
   - Random graphs

2. **Medium graphs (6-8 vertices)** - 400 cases
   - All above types
   - Star graphs
   - Bipartite graphs

3. **Larger graphs (9-12 vertices)** - 300 cases
   - Focus on trees, paths, cycles, and sparse graphs
   - Fewer complete/dense graphs (exact solution is slower)

## Output

The analysis generates:

1. **Statistical Summary**
   - Total test cases
   - Number of matches vs mismatches
   - Match rate percentage
   - Approximation accuracy

2. **Performance Metrics**
   - Path length differences (exact - approximation)
   - Approximation ratios (approximation / exact)
   - Runtime comparisons
   - Speedup analysis

3. **Detailed Analysis**
   - Top 50 worst approximation cases
   - Cases where approximation is < 80% of optimal
   - Individual case breakdowns

## Requirements

- Python 3.6+
- Both exact and approximation solution scripts must be present:
  - `exact_solution/cs412_longestpath_exact.py`
  - `approx_solution/cs412_longestpath_approx.py`

## Notes

- The exact solution uses exponential time, so test cases are limited to graphs with ≤12 vertices
- Larger graphs focus on sparse structures (trees, paths) where exact solution is faster
- The comparison includes hundreds of cases where the approximation fails to find the optimal solution
- All test cases are designed to be interesting and diverse, not just random

## Expected Results

The analysis should show:
- Hundreds of cases where approximation finds suboptimal solutions
- Various approximation ratios (some close to optimal, some significantly worse)
- Clear demonstration of the trade-off between solution quality and runtime
- Cases where greedy algorithms make poor choices early that lead to suboptimal paths

