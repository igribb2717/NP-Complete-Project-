#!/usr/bin/env python3
"""
Generate line graph for Exact solution only using Part D additional test cases.
"""

import os
import subprocess
import time
import sys
import csv

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Error: matplotlib is not installed.")
    print("Install with: pip install matplotlib numpy")
    sys.exit(1)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

EXACT_SCRIPT = os.path.join(PROJECT_ROOT, "exact_solution", "cs412_longestpath_exact.py")

TEST_DIR = os.path.join(PROJECT_ROOT, "part_D", "additional_test_cases")
CSV_FILE = os.path.join(PROJECT_ROOT, "part_D", "exact_only_comparison.csv")
PNG_FILE = os.path.join(PROJECT_ROOT, "part_D", "exact_only_comparison.png")
PDF_FILE = os.path.join(PROJECT_ROOT, "part_D", "exact_only_comparison.pdf")

# Timeout
EXACT_TIMEOUT = 60.0


def read_graph_size(path):
    """Read first line and return (n_vertices, n_edges)."""
    try:
        with open(path, "r") as f:
            first = f.readline().strip()
        if not first:
            return 0, 0
        parts = first.split()
        if len(parts) < 2:
            return 0, 0
        n = int(parts[0])
        m = int(parts[1])
        return n, m
    except:
        return 0, 0


def run_solver(script, input_path, timeout):
    """Run solver and return (success, runtime, path_length)."""
    start = time.time()
    try:
        with open(input_path, "r") as f:
            proc = subprocess.run(
                ["python3", script],
                stdin=f,
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


def generate_data():
    """Generate data and save to CSV."""
    if not os.path.isdir(TEST_DIR):
        print(f"Error: Test directory not found: {TEST_DIR}")
        sys.exit(1)

    # Get all .txt files, sorted
    test_files = sorted([f for f in os.listdir(TEST_DIR) if f.endswith(".txt")])
    
    if not test_files:
        print(f"Error: No test files found in {TEST_DIR}")
        sys.exit(1)

    print(f"Found {len(test_files)} test cases")
    print(f"Generating data...")
    print()

    data = []

    for test_file in test_files:
        test_path = os.path.join(TEST_DIR, test_file)
        n, m = read_graph_size(test_path)
        
        if n == 0 and m == 0:
            continue

        print(f"Running {test_file}: {n} vertices, {m} edges", end=" ... ", flush=True)

        # Run Exact
        exact_ok, exact_time, exact_len = run_solver(EXACT_SCRIPT, test_path, EXACT_TIMEOUT)
        if not exact_ok or exact_time >= EXACT_TIMEOUT * 0.9:
            print("TIMEOUT")
            continue

        data.append({
            "test_name": test_file,
            "vertices": n,
            "edges": m,
            "exact_time": exact_time,
            "exact_value": exact_len,
        })

        print(f"✓ ({exact_time:.3f}s, length={exact_len})")

    # Save to CSV
    with open(CSV_FILE, "w", newline="") as csvfile:
        fieldnames = ["test_name", "vertices", "edges", "exact_time", "exact_value"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print()
    print(f"Data saved to: {CSV_FILE}")
    return data


def plot_exact_only(data):
    """Create line graph for Exact solution runtime."""
    if not data:
        print("No data to plot.")
        return

    # Sort by complexity: edges first, then vertices
    data.sort(key=lambda d: (d["edges"], d["vertices"]))

    # Create uniform test names
    size_counts = {}
    uniform_names = []
    for d in data:
        v = d["vertices"]
        e = d["edges"]
        key = (v, e)
        if key not in size_counts:
            size_counts[key] = 0
        size_counts[key] += 1
        count = size_counts[key]

        if count == 1:
            uniform_names.append(f"{v}v_{e}")
        else:
            uniform_names.append(f"{v}v_{e}_{count}")

    exact_times = [d["exact_time"] for d in data]

    fig, ax = plt.subplots(1, 1, figsize=(max(16, len(data) * 0.65), 8))

    x_pos = range(len(data))

    ax.plot(x_pos, exact_times, "ro-", label="Exact (optimal)", linewidth=2.5, markersize=8, alpha=0.8)

    ax.set_xlabel("Test Case", fontsize=12, fontweight="bold")
    ax.set_ylabel("Runtime (seconds, log scale)", fontsize=12, fontweight="bold")
    ax.set_title("Exact Solution Runtime\n(Part D Additional Test Cases)", 
                 fontsize=14, fontweight="bold", pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(uniform_names, rotation=45, ha="right", fontsize=8)
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(loc="upper left", fontsize=11, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(PNG_FILE, dpi=300, bbox_inches="tight")
    plt.savefig(PDF_FILE, bbox_inches="tight")
    print(f"Graph saved to:\n  {PNG_FILE}\n  {PDF_FILE}")
    plt.close()


def main():
    print("=" * 80)
    print("Exact Solution Only - Part D Additional Test Cases")
    print("=" * 80)
    print()

    data = generate_data()

    if data:
        print()
        print("Generating line graph...")
        plot_exact_only(data)
        print()
        print("=" * 80)
        print("Complete!")
        print(f"CSV file: {CSV_FILE}")
        print(f"Graph files: {PNG_FILE}, {PDF_FILE}")
        print("=" * 80)
    else:
        print("No data generated.")


if __name__ == "__main__":
    main()

