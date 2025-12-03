#!/usr/bin/env python3
"""Compare baseline approximation vs improved on worst improved cases."""

import os
import subprocess
import sys
import csv

def run_solution(script_path, test_file, timeout=300):
    """Run a solution script on a test file and return the path length."""
    try:
        result = subprocess.run(
            [sys.executable, script_path, test_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode != 0:
            return None
        
        lines = result.stdout.strip().split('\n')
        if len(lines) < 1:
            return None
        
        try:
            path_length = int(lines[0])
            return path_length
        except ValueError:
            return None
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        return None

# Get paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
test_dir = os.path.join(script_dir, "part_e_test_cases")
baseline_script = os.path.join(project_root, "approx_solution", "cs412_longestpath_approx.py")
exact_script = os.path.join(project_root, "exact_solution", "cs412_longestpath_exact.py")

# Worst 5 cases for improved approximation
worst_cases = [
    'test_0944.txt',
    'test_0924.txt',
    'test_0896.txt',
    'test_0678.txt',
    'test_0957.txt'
]

results = []

print("Comparing Baseline vs Improved on Worst Improved Cases:")
print("=" * 80)

for test_file in worst_cases:
    test_path = os.path.join(test_dir, test_file)
    
    baseline_length = run_solution(baseline_script, test_path, timeout=30)
    exact_length = run_solution(exact_script, test_path, timeout=120)
    
    # Get improved results from JSON
    import json
    with open(os.path.join(script_dir, 'improved_approx_full_results.json'), 'r') as f:
        improved_data = json.load(f)
    
    improved_result = next((r for r in improved_data if r['test_file'] == test_file), None)
    improved_length = improved_result['improved_length'] if improved_result else None
    exact_length_from_json = improved_result['exact_length'] if improved_result else exact_length
    
    if baseline_length is not None and improved_length is not None and exact_length_from_json is not None:
        baseline_pct = (baseline_length / exact_length_from_json * 100) if exact_length_from_json > 0 else 0
        improved_pct = (improved_length / exact_length_from_json * 100) if exact_length_from_json > 0 else 0
        
        results.append({
            'test_file': test_file,
            'baseline_length': baseline_length,
            'improved_length': improved_length,
            'exact_length': exact_length_from_json,
            'baseline_pct': baseline_pct,
            'improved_pct': improved_pct,
            'baseline_better': baseline_length > improved_length
        })
        
        print(f"\n{test_file}:")
        print(f"  Baseline: {baseline_length} ({baseline_pct:.2f}%)")
        print(f"  Improved: {improved_length} ({improved_pct:.2f}%)")
        print(f"  Exact:    {exact_length_from_json}")
        print(f"  Baseline better: {baseline_length > improved_length}")

# Create CSV
csv_file = os.path.join(script_dir, "baseline_vs_improved_worst.csv")
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Test File', 'Baseline Length', 'Improved Length', 'Exact Length', 
                     'Baseline %', 'Improved %', 'Baseline Better'])
    for r in results:
        writer.writerow([
            r['test_file'],
            r['baseline_length'],
            r['improved_length'],
            r['exact_length'],
            f"{r['baseline_pct']:.2f}%",
            f"{r['improved_pct']:.2f}%",
            r['baseline_better']
        ])

print(f"\n\nResults saved to: {csv_file}")

