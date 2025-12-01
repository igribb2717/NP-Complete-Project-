# Approximation Error Percentage Analysis

## Overview

This analysis calculates how well your approximation algorithm performs compared to the exact (optimal) solution. The error percentage metric helps identify where the algorithm needs improvement.

## Error Percentage Metric

**Formula:** `Error % = (Approximate Value / Exact Value) × 100`

**Interpretation:**
- **100.00%** = Perfect (found optimal solution)
- **95.00%** = Approximation is 5% worse than optimal
- **90.00%** = Approximation is 10% worse than optimal
- **< 90%** = Poor performance (needs significant improvement)

## How to Run

1. **Generate run data** (if not already done):
   ```bash
   python3 part_D/run_part_D_runtime_study.py
   ```

2. **Analyze error percentages**:
   ```bash
   python3 part_D/analyze_error_percentage.py
   ```

3. **View results**:
   - Quick summary: `part_D/error_analysis_summary.txt`
   - Detailed report: `part_D/error_analysis_report.txt`

## Output Files

### `error_analysis_summary.txt`
Quick reference with:
- Overall average error percentage
- Percentage of runs finding optimal solutions
- Average error by test size (vertices × edges)

### `error_analysis_report.txt`
Comprehensive report including:
- Metric explanation
- Overall statistics (average, min, max, std dev)
- Statistics grouped by test size
- Detailed results for each test case
- Recommendations for algorithm improvement

## Using Results to Improve the Algorithm

### Step 1: Identify Problem Areas

Look at the **"STATISTICS BY TEST SIZE"** section to find:
- Test sizes with lowest average error % (worst performance)
- Test sizes with high standard deviation (inconsistent performance)

**Example from your results:**
- `10 vertices, 20 edges`: 96.40% average (needs improvement)
- `9 vertices, 15 edges`: 98.81% average (could be better)

### Step 2: Examine Specific Test Cases

Check the **"DETAILED RESULTS BY TEST CASE"** section to find:
- Individual test cases with low error percentages
- Cases where min/max error varies significantly (inconsistent)

**Example:**
- `test_input_6` (10v, 20e): 93.69% - This is your worst case!

### Step 3: Analyze the Problem Cases

For each problematic test case:

1. **Run the exact solver** to see the optimal path:
   ```bash
   python3 exact_solution/cs412_longestpath_exact.py timing_tests/test_cases/test_05.txt
   ```

2. **Run the approximation** multiple times to see what it finds:
   ```bash
   python3 approx_solution/cs412_longestpath_approx.py timing_tests/test_cases/test_05.txt
   ```

3. **Compare the paths**:
   - What makes the optimal path better?
   - What pattern does the approximation miss?
   - Are there high-weight edges the approximation ignores?

### Step 4: Modify the Algorithm

Based on your analysis, consider:

1. **Increase exploration**:
   - Try more starting vertices
   - Try more random seeds per start
   - Try different tie-breaking strategies

2. **Improve greedy strategy**:
   - Add lookahead (already implemented)
   - Consider 2-step or 3-step lookahead
   - Weight edges by connectivity (prefer vertices with many high-weight edges)

3. **Hybrid approaches**:
   - Combine multiple strategies
   - Use exact solver for small subgraphs
   - Post-process with local search

4. **Target specific problem sizes**:
   - If 10 vertices, 20 edges is problematic, add special handling
   - Adjust parameters based on graph density

### Step 5: Re-run and Compare

After making changes:

1. Re-run the runtime study:
   ```bash
   python3 part_D/run_part_D_runtime_study.py
   ```

2. Re-analyze errors:
   ```bash
   python3 part_D/analyze_error_percentage.py
   ```

3. Compare before/after:
   - Did overall average improve?
   - Did problematic test sizes improve?
   - Did you introduce regressions in other areas?

## Current Performance Summary

Based on your latest run:
- **Overall Average Error: 99.53%** (excellent!)
- **Optimal Solutions Found: 78.9%** of runs
- **Worst Test Size: 10 vertices, 20 edges** (96.40% average)
- **Worst Individual Case: test_input_6** (93.69%)

## Recommendations

1. **Focus on 10-vertex, 20-edge graphs** - This is your weakest area
2. **Investigate test_input_6** - Why does it consistently underperform?
3. **Consider increasing exploration** for medium-sized graphs (9-11 vertices)
4. **Maintain current performance** on smaller graphs (excellent results!)

## Files Reference

- `comparison_runs_part_D.txt` - Raw individual run data (test|solver|run|time|value)
- `comparison_data_part_D.txt` - Averaged data used for plots
- `error_analysis_report.txt` - Detailed analysis report
- `error_analysis_summary.txt` - Quick summary


