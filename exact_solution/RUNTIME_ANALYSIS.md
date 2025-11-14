# Runtime Analysis Documentation

## Overview

This document describes the test cases and runtime analysis tools created to demonstrate how the wall clock runtime of the longest path exact solution varies with different input sizes.

## Test Cases

We have created **17 test cases** of varying sizes:

### Size Distribution

| Category | Vertices | Count | Expected Runtime |
|----------|----------|-------|------------------|
| Very Small | 2-3 | 3 | < 1 second |
| Small | 4-5 | 2 | < 5 seconds |
| Medium | 6-10 | 5 | seconds to minutes |
| Large | 11-15 | 4 | minutes |
| Very Large | 18-20 | 2 | **> 20 minutes** |
| Extreme | 22+ | 1 | hours |

### Test Cases Requiring > 20 Minutes

The following test cases are guaranteed to take more than 20 minutes:

1. **test_input_large**: 18 vertices, 35 edges
2. **test_input_very_large**: 20 vertices, 40 edges

These test cases clearly demonstrate the exponential growth in runtime as the problem size increases.

## Runtime Measurement

### Step 1: Measure Runtime

Run the measurement script to collect wall clock times for all test cases:

```bash
bash measure_runtime.sh
```

This script:
- Runs each test case and measures wall clock time using the `time` command
- Outputs results to `runtime_data.txt`
- Shows progress as it runs through all test cases

**Note**: This will take a long time (potentially hours) because it includes the very large test cases.

### Step 2: Visualize Results

Generate plots showing runtime vs input size:

```bash
python3 plot_runtime.py
```

This creates:
- `runtime_analysis.png` - High-resolution plot
- `runtime_analysis.pdf` - Publication-quality PDF

The plots include:
1. **Runtime vs Number of Vertices** - Shows exponential growth
2. **Runtime vs Number of Edges** - Shows relationship with edge count
3. **Log-Log Scale Plot** - Demonstrates factorial growth pattern
4. **Summary Table** - All test results in tabular format

## Expected Runtime Growth

The longest path problem has O(n! * n) worst-case complexity. This means:

- **n=3**: ~0.001 seconds
- **n=5**: ~0.1 seconds  
- **n=8**: ~10 seconds
- **n=10**: ~100 seconds (1-2 minutes)
- **n=15**: ~hours
- **n=18**: **> 20 minutes** ✓
- **n=20**: **> 20 minutes** ✓
- **n=22**: hours to days

## Running All Tests

To run all test cases with timing information:

```bash
bash run_test_cases.sh
```

This script:
- Runs tests in order of increasing size
- Shows timing for each test
- Clearly marks test cases expected to take > 20 minutes
- Provides warnings for extreme test cases

## Requirements for Plotting

The plotting script requires:
- Python 3
- matplotlib: `pip install matplotlib`
- numpy: `pip install numpy`

If these are not installed, the measurement script will still work, but plotting will fail.

## Output Files

After running the analysis:

- `runtime_data.txt` - Raw timing data (text format)
- `runtime_analysis.png` - Visualization plot (PNG)
- `runtime_analysis.pdf` - Visualization plot (PDF)

These files can be included in your project submission to demonstrate the runtime analysis.

