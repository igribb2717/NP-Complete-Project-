#!/usr/bin/env python3
"""Quick test of comparison on a small sample of test cases."""

import subprocess
import os

# Test on first 10 cases
test_dir = "part_e_test_cases"
test_files = sorted([f for f in os.listdir(test_dir) if f.endswith('.txt')])[:10]

print(f"Testing comparison on {len(test_files)} sample cases...\n")

for test_file in test_files:
    test_path = os.path.join(test_dir, test_file)
    
    # Run exact
    exact_result = subprocess.run(
        ['python3', 'exact_solution/cs412_longestpath_exact.py', test_path],
        capture_output=True, text=True, timeout=10
    )
    
    # Run approx
    approx_result = subprocess.run(
        ['python3', 'approx_solution/cs412_longestpath_approx.py', test_path],
        capture_output=True, text=True, timeout=5
    )
    
    if exact_result.returncode == 0 and approx_result.returncode == 0:
        exact_len = int(exact_result.stdout.split('\n')[0])
        approx_len = int(approx_result.stdout.split('\n')[0])
        match = "✓" if exact_len == approx_len else "✗"
        diff = exact_len - approx_len
        print(f"{test_file}: Exact={exact_len}, Approx={approx_len}, Diff={diff} {match}")
    else:
        print(f"{test_file}: ERROR")

print("\nSample test complete!")

