# Part E: Comprehensive Test Case Comparison - Summary

## Overview

This implementation generates **1090+ test cases** and performs a comprehensive comparison between the exact (optimal) and approximation solutions for the Longest Path problem.

## Generated Files

### Scripts
1. **`generate_test_cases.py`** - Generates 1090+ diverse test cases
   - Small graphs (3-5 vertices): ~350 cases
   - Medium graphs (6-8 vertices): ~450 cases  
   - Larger graphs (9-12 vertices): ~300 cases
   - Includes: complete graphs, trees, paths, cycles, sparse/dense graphs, greedy trap graphs, star graphs, bipartite graphs, random graphs

2. **`run_comparison.py`** - Runs both solutions on all test cases
   - Executes exact solution on each test case
   - Executes approximation solution on each test case
   - Collects results and saves to JSON

3. **`analyze_comparison.py`** - Analyzes results and generates comprehensive report
   - Statistical analysis (differences, ratios, runtimes)
   - Identifies worst approximation cases
   - Finds cases where approximation is < 80% of optimal
   - Generates detailed text report

4. **`run_part_e.sh`** - Master script that runs all steps in sequence

### Output Files (generated when scripts run)
- `part_e_test_cases/` - Directory with 1090+ test case files
- `part_e_comparison_results.json` - Raw comparison data
- `part_e_comparison_report.txt` - Comprehensive analysis report

## Test Case Diversity

The generator creates test cases designed to:
- **Show approximation successes**: Cases where greedy algorithm finds optimal solution
- **Show approximation failures**: Cases where greedy makes poor choices (hundreds of these)
- **Cover various graph structures**: Trees, cycles, complete graphs, sparse/dense graphs
- **Include "greedy trap" graphs**: Specifically designed to fool greedy algorithms

## Expected Results

When you run the full comparison, you should see:
- **Hundreds of cases where approximation fails** to find the optimal solution
- **Various approximation ratios**: Some close to 1.0 (optimal), some significantly lower
- **Clear demonstration** of the trade-off between solution quality and runtime
- **Statistical analysis** showing mean/median differences and ratios
- **Top 50 worst cases** where approximation performs poorly
- **Cases where approximation is < 80% of optimal** (should be hundreds)

## How to Run

### Quick Test (10 cases)
```bash
python3 test_comparison_sample.py
```

### Full Analysis (1090+ cases - may take 30-60 minutes)
```bash
./run_part_e.sh
```

Or step by step:
```bash
# Step 1: Generate test cases (fast, ~1 minute)
python3 generate_test_cases.py

# Step 2: Run comparison (slow, 30-60 minutes depending on hardware)
python3 run_comparison.py

# Step 3: Analyze results (fast, ~1 minute)
python3 analyze_comparison.py
```

## Key Features

1. **Comprehensive Coverage**: 1090+ test cases covering many graph types and sizes
2. **Designed to Show Failures**: Includes many "greedy trap" graphs that specifically cause approximation to fail
3. **Statistical Analysis**: Detailed statistics on differences, ratios, and performance
4. **Detailed Reporting**: Identifies worst cases and provides individual case breakdowns
5. **Automated**: Single script runs everything end-to-end

## Notes

- The exact solution is exponential time, so test cases are limited to graphs with ≤12 vertices
- Larger graphs focus on sparse structures (trees, paths) where exact solution is faster
- The comparison includes timeout handling (60s for exact, 10s for approximation)
- All test cases use reproducible random seeds for consistency

## Verification

A sample test on 10 cases showed the comparison system works correctly. The full run will identify all cases where the approximation differs from the optimal solution, which should number in the hundreds based on the diverse test case generation strategy.

