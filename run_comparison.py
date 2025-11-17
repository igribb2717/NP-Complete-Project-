#!/usr/bin/env python3
"""
Comparison Runner for Exact vs Approximation Solutions
Runs both solutions on all test cases and collects results.
"""

import os
import subprocess
import json
import time
from pathlib import Path

def run_solution(script_path, test_file, timeout=300):
    """Run a solution script on a test file and return the result."""
    try:
        start_time = time.time()
        result = subprocess.run(
            ['python3', script_path, test_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        elapsed = time.time() - start_time
        
        if result.returncode != 0:
            return {
                'success': False,
                'error': result.stderr,
                'time': elapsed
            }
        
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:
            return {
                'success': False,
                'error': 'Invalid output format',
                'time': elapsed
            }
        
        try:
            path_length = int(lines[0])
            path = lines[1].split() if len(lines) > 1 and lines[1] else []
        except ValueError:
            return {
                'success': False,
                'error': 'Could not parse path length',
                'time': elapsed
            }
        
        return {
            'success': True,
            'path_length': path_length,
            'path': path,
            'time': elapsed
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Timeout',
            'time': timeout
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'time': 0
        }

def main():
    """Run comparison on all test cases."""
    test_dir = "part_e_test_cases"
    exact_script = "exact_solution/cs412_longestpath_exact.py"
    approx_script = "approx_solution/cs412_longestpath_approx.py"
    output_file = "part_e_comparison_results.json"
    
    if not os.path.exists(test_dir):
        print(f"Error: Test directory {test_dir} not found!")
        print("Please run generate_test_cases.py first.")
        return
    
    # Get all test files
    test_files = sorted([f for f in os.listdir(test_dir) if f.endswith('.txt')])
    
    if not test_files:
        print(f"Error: No test files found in {test_dir}!")
        return
    
    print(f"Found {len(test_files)} test cases")
    print(f"Running comparison (this may take a while)...")
    print()
    
    results = []
    exact_failures = 0
    approx_failures = 0
    matches = 0
    mismatches = 0
    
    for i, test_file in enumerate(test_files):
        test_path = os.path.join(test_dir, test_file)
        
        if (i + 1) % 100 == 0:
            print(f"Progress: {i + 1}/{len(test_files)} test cases processed...")
        
        # Run exact solution
        exact_result = run_solution(exact_script, test_path, timeout=60)
        
        # Run approximation solution
        approx_result = run_solution(approx_script, test_path, timeout=10)
        
        result_entry = {
            'test_file': test_file,
            'exact': exact_result,
            'approx': approx_result
        }
        
        # Analyze results
        if exact_result['success'] and approx_result['success']:
            exact_len = exact_result['path_length']
            approx_len = approx_result['path_length']
            
            if exact_len == approx_len:
                matches += 1
                result_entry['match'] = True
                result_entry['difference'] = 0
                result_entry['ratio'] = 1.0
            else:
                mismatches += 1
                result_entry['match'] = False
                result_entry['difference'] = exact_len - approx_len
                result_entry['ratio'] = approx_len / exact_len if exact_len > 0 else 0.0
        else:
            if not exact_result['success']:
                exact_failures += 1
            if not approx_result['success']:
                approx_failures += 1
            result_entry['match'] = None
        
        results.append(result_entry)
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print()
    print("=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    print(f"Total test cases: {len(test_files)}")
    print(f"Exact solution failures: {exact_failures}")
    print(f"Approximation solution failures: {approx_failures}")
    print(f"Cases where results match: {matches}")
    print(f"Cases where results differ: {mismatches}")
    print()
    print(f"Results saved to: {output_file}")
    print()
    print("Next step: Run analyze_comparison.py to generate detailed analysis")

if __name__ == "__main__":
    main()

