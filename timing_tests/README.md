# Timing Test Suite

This test suite measures the execution time of the approximation solution on progressively larger graphs.

## Test Cases

The suite contains 10 test cases that progress from:
- **Test 1**: 10 vertices, 45 edges
- **Test 2**: 11 vertices, 50 edges
- **Test 3**: 11 vertices, 55 edges
- **Test 4**: 12 vertices, 60 edges
- **Test 5**: 12 vertices, 66 edges
- **Test 6**: 13 vertices, 70 edges
- **Test 7**: 13 vertices, 75 edges
- **Test 8**: 13 vertices, 78 edges
- **Test 9**: 14 vertices, 80 edges
- **Test 10**: 14 vertices, 80 edges

Note: Since an undirected graph with n vertices can have at most n*(n-1)/2 edges, 
we increase the vertex count beyond 12 to accommodate 80 edges (12 vertices max = 66 edges).

Each test case is a randomly generated sparse graph with edge weights between 1 and 100.

## How to Run

### Step 1: Generate Test Cases

First, generate the test case files:

```bash
cd timing_tests
python3 generate_timing_tests.py
```

This will create a `test_cases/` directory with 10 test files (`test_01.txt` through `test_10.txt`).

### Step 2: Run the Timing Tests

Run the timing test suite:

**Using the approximation solution (default, faster):**
```bash
./run_timing_tests.sh
# or
./run_timing_tests.sh --approx
```

**Using the exact solution (slower, optimal):**
```bash
./run_timing_tests.sh --exact
```

Or if the script is not executable:

```bash
bash run_timing_tests.sh [--exact|--approx]
```

## Output

The script will:
1. Run each test case sequentially
2. Display the number of vertices and edges for each test
3. Show the execution time in minutes and seconds
4. Print a summary with the total time for all tests

Example output:
```
Test 1: 10 vertices, 60 edges
Running... Completed
  Duration: 2 seconds
  Vertices: 10, Edges: 60

Test 2: 10 vertices, 62 edges
Running... Completed
  Duration: 3 seconds
  Vertices: 10, Edges: 62

...

All tests completed!
Total time: 1 minute(s) 15 second(s)
```

## Notes

- By default, the tests run the **approximation solution** from `../approx_solution/cs412_longestpath_approx.py`
- Use `--exact` flag to run the **exact solution** from `../exact_solution/cs412_longestpath_exact.py` (will be slower)
- Test output is suppressed (redirected to `/dev/null`) to focus on timing information
- If you need to see the actual solution output, you can modify the script to remove the redirection

