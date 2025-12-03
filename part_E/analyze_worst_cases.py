#!/usr/bin/env python3
"""
Analyze worst performing test cases for approximation solution.
Finds the 5 worst cases where approximation performs worst compared to exact solution.
"""

import os
import subprocess
import csv
import sys
from pathlib import Path

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
        print(f"Error running {script_path} on {test_file}: {e}")
        return None

def main():
    """Main analysis function."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    test_dir = os.path.join(script_dir, "part_e_test_cases")
    # Paths relative to project root (where run_comparison.py expects them)
    exact_script = os.path.join(project_root, "exact_solution", "cs412_longestpath_exact.py")
    approx_script = os.path.join(project_root, "approx_solution", "cs412_longestpath_approx.py")
    
    if not os.path.exists(test_dir):
        print(f"Error: Test directory {test_dir} not found!")
        return
    
    if not os.path.exists(exact_script):
        print(f"Error: Exact solution script {exact_script} not found!")
        return
    
    if not os.path.exists(approx_script):
        print(f"Error: Approximation solution script {approx_script} not found!")
        return
    
    # Get all test files
    test_files = sorted([f for f in os.listdir(test_dir) if f.endswith('.txt')])
    
    if not test_files:
        print(f"Error: No test files found in {test_dir}!")
        return
    
    print(f"Found {len(test_files)} test cases")
    print("Running analysis (this may take a while)...")
    print()
    
    results = []
    
    for i, test_file in enumerate(test_files):
        test_path = os.path.join(test_dir, test_file)
        
        if (i + 1) % 100 == 0:
            print(f"Progress: {i + 1}/{len(test_files)} test cases processed...")
        
        # Run approximation solution
        approx_length = run_solution(approx_script, test_path, timeout=10)
        
        # Run exact solution
        exact_length = run_solution(exact_script, test_path, timeout=60)
        
        if approx_length is not None and exact_length is not None:
            ratio = approx_length / exact_length if exact_length > 0 else 0.0
            difference = exact_length - approx_length
            
            results.append({
                'test_file': test_file,
                'approx_length': approx_length,
                'exact_length': exact_length,
                'ratio': ratio,
                'difference': difference
            })
        elif approx_length is None:
            print(f"Warning: Approximation failed on {test_file}")
        elif exact_length is None:
            print(f"Warning: Exact solution failed on {test_file}")
    
    print(f"\nSuccessfully processed {len(results)} test cases")
    
    # Sort by worst performance (lowest ratio, then largest difference)
    results.sort(key=lambda x: (x['ratio'], -x['difference']))
    
    # Get the 5 worst cases
    worst_5 = results[:5]
    
    print("\n5 Worst Performing Cases (by ratio):")
    print("-" * 80)
    for i, case in enumerate(worst_5, 1):
        print(f"{i}. {case['test_file']}")
        print(f"   Approximation: {case['approx_length']}, Exact: {case['exact_length']}")
        print(f"   Ratio: {case['ratio']:.4f} ({case['ratio']*100:.2f}%)")
        print(f"   Difference: {case['difference']}")
        print()
    
    # Write CSV for worst 5 approximation lengths
    approx_csv_file = os.path.join(script_dir, "worst_5_approx_lengths.csv")
    with open(approx_csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Test File', 'Approximation Length'])
        for case in worst_5:
            writer.writerow([case['test_file'], case['approx_length']])
    
    print(f"Created {approx_csv_file}")
    
    # Write CSV for worst 5 exact lengths
    exact_csv_file = os.path.join(script_dir, "worst_5_exact_lengths.csv")
    with open(exact_csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Test File', 'Exact Length'])
        for case in worst_5:
            writer.writerow([case['test_file'], case['exact_length']])
    
    print(f"Created {exact_csv_file}")
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()

