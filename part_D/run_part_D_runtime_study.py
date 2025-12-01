#!/usr/bin/env python3
"""
Part D runtime study:

- Runs the exact and approximation solvers on a wider variety of test cases,
  including timing tests.
- Repeats each run multiple times and averages wall-clock runtime to smooth noise.
- Writes a comparison data file in the same format as `comparison_data.txt`:

  test_name|vertices|edges|exact_time|approx_time|exact_length|approx_length|quality|diff|percent|speedup

Output file:
  part_D/comparison_data_part_D.txt

You can then generate plots with:
  python3 part_D/plot_part_D.py
"""

import os
import subprocess
import time
import math

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # this is part_D
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)  # actual project root

EXACT_SCRIPT = os.path.join(PROJECT_ROOT, "exact_solution", "cs412_longestpath_exact.py")
APPROX_SCRIPT = os.path.join(PROJECT_ROOT, "approx_solution", "cs412_longestpath_approx.py")

OUTPUT_FILE = os.path.join(PROJECT_ROOT, "part_D", "comparison_data_part_D.txt")
RUNS_LOG_FILE = os.path.join(PROJECT_ROOT, "part_D", "comparison_runs_part_D.txt")

# Number of times to repeat each run to average runtime
REPEATS = 5

# Timeouts (seconds) to avoid hanging forever on very hard instances
EXACT_TIMEOUT = 60.0  # 60 seconds max per run (5 repeats = up to 5 minutes per test)
APPROX_TIMEOUT = 30.0

# Skip test cases that are too large (will likely timeout)
# Format: (max_vertices, max_edges) - skip if test exceeds both
MAX_TEST_SIZE = (11, 55)  # Skip anything with >11 vertices OR >55 edges


def read_graph_size(path):
    """Read first line of a test file and return (n_vertices, n_edges)."""
    with open(path, "r") as f:
        first = f.readline().strip()
    if not first:
        return 0, 0
    parts = first.split()
    if len(parts) < 2:
        return 0, 0
    try:
        n = int(parts[0])
        m = int(parts[1])
    except ValueError:
        return 0, 0
    return n, m


def run_solver(script, input_path, timeout):
    """
    Run a solver once on a given input file.
    Returns (success, runtime_seconds, path_length_int_or_0).
    """
    start = time.time()
    try:
        proc = subprocess.run(
            ["python3", script, input_path],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = time.time() - start
    except subprocess.TimeoutExpired:
        return False, timeout, 0
    except Exception:
        return False, 0.0, 0

    if proc.returncode != 0:
        return False, elapsed, 0

    lines = proc.stdout.strip().splitlines()
    if not lines:
        return False, elapsed, 0

    try:
        length = int(lines[0].strip().split()[0])
    except ValueError:
        length = 0

    return True, elapsed, length


def avg_over_repeats(script, input_path, timeout, repeats, solver_name, test_name, runs_log):
    """
    Run solver multiple times and return (avg_time, length_from_best_run).
    Also logs each individual run (non-averaged) to runs_log.
    """
    times = []
    best_len = 0
    for i in range(repeats):
        run_idx = i + 1
        success, t, length = run_solver(script, input_path, timeout)
        if not success:
            # Treat as timeout for averaging/logging
            t = timeout
            length = 0
        times.append(t)
        if length > best_len:
            best_len = length
        # Log this individual run
        runs_log.write(
            f"{test_name}|{solver_name}|run_{run_idx}|{t:.6f}|{length}\n"
        )
    avg_time = sum(times) / len(times) if times else 0.0
    return avg_time, best_len


def main():
    # Collect a mix of small/medium/large-ish cases
    tests = []

    # Existing comparison tests from approx_solution/test_cases
    approx_cases_dir = os.path.join(PROJECT_ROOT, "approx_solution", "test_cases")
    base_cases = [
        "test_small_1",
        "test_small_2",
        "test_medium_1",
        "test_medium_2",
        "test_large_1",
        "test_nonoptimal",
    ]
    for name in base_cases:
        path = os.path.join(approx_cases_dir, name)
        if os.path.exists(path):
            tests.append(path)

    # Add some manageable test cases from exact_solution/test_cases
    exact_cases_dir = os.path.join(PROJECT_ROOT, "exact_solution", "test_cases")
    exact_cases = [
        "test_input_1",      # 3 vertices, 3 edges
        "test_input_2",      # 4 vertices, 6 edges
        "test_input_3",      # 5 vertices, 10 edges
        "test_input_4",      # 6 vertices, 9 edges
        "test_input_5",      # 8 vertices, 12 edges
        "test_input_6",      # 10 vertices, 20 edges
        "test_input_small_1",
        "test_input_small_2",
        "test_input_medium_1",
        "test_input_medium_2",
    ]
    for name in exact_cases:
        path = os.path.join(exact_cases_dir, name)
        if os.path.exists(path):
            n, m = read_graph_size(path)
            # Only add if not too large
            if n <= MAX_TEST_SIZE[0] and m <= MAX_TEST_SIZE[1]:
                tests.append(path)
            else:
                print(f"Skipping {name}: {n} vertices, {m} edges (too large)")

    # Timing tests (10–14 vertices, up to ~80 edges)
    # Filter out cases that are too large to avoid timeouts
    timing_dir = os.path.join(PROJECT_ROOT, "timing_tests", "test_cases")
    if os.path.isdir(timing_dir):
        for fname in sorted(os.listdir(timing_dir)):
            if fname.startswith("test_") and fname.endswith(".txt"):
                path = os.path.join(timing_dir, fname)
                n, m = read_graph_size(path)
                # Skip if too large
                if n > MAX_TEST_SIZE[0] or m > MAX_TEST_SIZE[1]:
                    print(f"Skipping {fname}: {n} vertices, {m} edges (too large, will timeout)")
                    continue
                tests.append(path)

    # Additional test cases (8-11 vertices, 3 examples each)
    additional_dir = os.path.join(PROJECT_ROOT, "part_D", "additional_test_cases")
    if os.path.isdir(additional_dir):
        for fname in sorted(os.listdir(additional_dir)):
            if fname.endswith(".txt"):
                path = os.path.join(additional_dir, fname)
                n, m = read_graph_size(path)
                # Skip if too large
                if n > MAX_TEST_SIZE[0] or m > MAX_TEST_SIZE[1]:
                    print(f"Skipping {fname}: {n} vertices, {m} edges (too large, will timeout)")
                    continue
                tests.append(path)

    if not tests:
        print("No test cases found for Part D runtime study.")
        return

    # De-duplicate and sort
    tests = sorted(set(tests))

    # Check which tests have already been run
    existing_tests = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("|")
                if len(parts) >= 1:
                    existing_tests.add(parts[0])
    
    # Filter to only new tests (those not in existing data)
    new_tests = [t for t in tests if os.path.basename(t) not in existing_tests]
    tests_to_run = new_tests if new_tests else tests
    
    print(f"Found {len(tests)} total test files.")
    if existing_tests:
        print(f"  {len(existing_tests)} already have results (will be preserved)")
        print(f"  {len(tests_to_run)} new tests to run")
    else:
        print(f"  Running all {len(tests_to_run)} tests")

    # Open file in append mode if we have existing data, otherwise write mode
    file_mode = "a" if existing_tests and tests_to_run else "w"
    
    with open(OUTPUT_FILE, file_mode) as out, open(RUNS_LOG_FILE, "a" if existing_tests else "w") as runs_log:
        # Only write header if starting fresh
        if file_mode == "w":
            out.write(
                "# Test Case | Vertices | Edges | Exact Runtime (s) | Approx Runtime (s) | "
                "Exact Value | Approx Value | Quality | Difference | Percent Diff | Speedup\n"
            )
            out.write(
                "# Format: test_name|vertices|edges|exact_time|approx_time|"
                "exact_length|approx_length|quality|diff|percent|speedup\n\n"
            )

        for path in tests_to_run:
            test_name = os.path.basename(path)
            n, m = read_graph_size(path)
            print(f"\nRunning test {test_name}: {n} vertices, {m} edges")
            print(f"  Running exact solver ({REPEATS} repeats, timeout={EXACT_TIMEOUT}s)...")

            # Exact solver
            exact_time, exact_len = avg_over_repeats(
                EXACT_SCRIPT, path, EXACT_TIMEOUT, REPEATS,
                solver_name="exact", test_name=test_name, runs_log=runs_log
            )
            if exact_time >= EXACT_TIMEOUT * 0.9:  # Close to timeout
                print(f"  WARNING: Exact solver timed out or took very long ({exact_time:.2f}s)")
            else:
                print(f"  Exact: {exact_time:.4f}s avg, path length = {exact_len}")

            print(f"  Running approx solver ({REPEATS} repeats, timeout={APPROX_TIMEOUT}s)...")
            # Approx solver
            approx_time, approx_len = avg_over_repeats(
                APPROX_SCRIPT, path, APPROX_TIMEOUT, REPEATS,
                solver_name="approx", test_name=test_name, runs_log=runs_log
            )
            if approx_time >= APPROX_TIMEOUT * 0.9:
                print(f"  WARNING: Approx solver timed out or took very long ({approx_time:.2f}s)")
            else:
                print(f"  Approx: {approx_time:.4f}s avg, path length = {approx_len}")

            # Quality metrics
            if exact_len == approx_len:
                quality = "OPTIMAL"
                diff = 0
                percent = 0.0
            else:
                quality = "SUBOPTIMAL"
                diff = exact_len - approx_len
                percent = (diff * 100.0 / exact_len) if exact_len > 0 else 0.0

            # Speedup = exact / approx
            if approx_time > 0 and exact_time > 0:
                speedup = exact_time / approx_time
                speedup_str = f"{speedup:.2f}"
            else:
                speedup_str = "N/A"

            # Only write if we got valid results (didn't timeout on both)
            if exact_time < EXACT_TIMEOUT * 0.9 or approx_time < APPROX_TIMEOUT * 0.9:
                line = (
                    f"{test_name}|{n}|{m}|{exact_time:.6f}|{approx_time:.6f}|"
                    f"{exact_len}|{approx_len}|{quality}|{diff}|{percent:.2f}|{speedup_str}\n"
                )
                out.write(line)
                print(f"  ✓ Results written")
            else:
                print(f"  ✗ Skipping (both solvers timed out)")

    print("Part D runtime study complete.")
    print("Now run:")
    print("  python3 part_D/plot_part_D.py")


if __name__ == "__main__":
    main()


