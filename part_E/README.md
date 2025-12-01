# Part E: Augment the Study - Improved Approximation Solution

This folder contains the comprehensive comparison study and an improved version of the approximation algorithm.

## Overview

Part E includes:
1. **1000+ test cases** - Comprehensive test suite in `part_e_test_cases/`
2. **Improved approximation solution** - Enhanced algorithm that improves performance on difficult cases
3. **Comparison tools** - Scripts to compare original vs improved vs exact solutions

## Files

### Improved Solution
- **`cs412_longestpath_approx_improved.py`** - Enhanced approximation algorithm with clear comments explaining improvements

### Comparison Scripts
- **`run_comparison_improved.py`** - Compares exact, original approx, and improved approx on all test cases
- **`generate_test_cases.py`** - Generates 1000+ diverse test cases (moved from root)
- **`run_comparison.py`** - Original comparison script (moved from root)
- **`analyze_comparison.py`** - Analysis script (moved from root)
- **`run_part_e.sh`** - Master script to run everything (moved from root)

### Test Cases
- **`part_e_test_cases/`** - Directory containing 1091+ test case files

### Documentation
- **`PART_E_README.md`** - Original Part E documentation
- **`PART_E_SUMMARY.md`** - Summary of Part E implementation

## Improvements Made to Approximation Algorithm

The improved solution (`cs412_longestpath_approx_improved.py`) includes the following enhancements:

### 1. Enhanced 2-Step Lookahead
- **Original**: 1-step lookahead with 0.3 weight
- **Improved**: 2-step lookahead that considers paths 2 edges ahead
- **Benefit**: Helps avoid getting trapped in local optima by seeing further ahead

### 2. Backtracking on Dead Ends
- **Original**: Stops when no neighbors available
- **Improved**: When path ends early, backtracks one step and explores alternative paths
- **Benefit**: Recovers from poor early choices

### 3. High-Degree Vertex Prioritization
- **Original**: Randomly samples starting vertices
- **Improved**: Prioritizes starting from vertices with high degree (many edges)
- **Benefit**: High-degree vertices often lead to better paths

### 4. Increased Exploration for Medium Graphs
- **Original**: Fixed number of seeds per start
- **Improved**: More seeds for graphs in the 8-12 vertex range (problematic size)
- **Benefit**: Increases chance of finding optimal paths for difficult sizes

### 5. Path Extension Strategy
- **Original**: Only extends forward
- **Improved**: Also tries "reverse" paths (builds path backwards from end vertex)
- **Benefit**: Explores different path structures

## Target Test Cases

These improvements specifically target the worst-performing test cases identified in Part D error analysis:
- **test_input_6** (10v, 20e): 93.69% accuracy → target: improve to >95%
- **10 vertices, 20 edges**: 96.40% average → target: improve to >98%
- **9 vertices, 15 edges**: 98.81% average → target: improve to >99%

## How to Run

### Quick Test (Single Test Case)
```bash
# Test on a specific case
python3 part_E/cs412_longestpath_approx_improved.py exact_solution/test_cases/test_input_6
```

### Full Comparison (All 1000+ Test Cases)
```bash
cd part_E
python3 run_comparison_improved.py
```

This will:
1. Run exact solution on all test cases
2. Run original approximation on all test cases
3. Run improved approximation on all test cases
4. Compare results and identify improvements
5. Generate `comparison_improved.json` and `improvement_report.txt`

### Generate Test Cases (if needed)
```bash
cd part_E
python3 generate_test_cases.py
```

## Expected Results

The improved algorithm should:
- **Improve at least one test case** compared to the original
- Show better performance on 10-vertex, 20-edge graphs (the worst case)
- Maintain or improve performance on other test cases
- Demonstrate clear improvements in the comparison report

## Verification

To verify the improvement works:
1. Run the comparison script
2. Check `improvement_report.txt` for cases where improved version is better
3. Look for test cases where improved found optimal but original didn't
4. Verify that at least one test case shows improvement

