#!/usr/bin/env python3
"""
Part E: Comprehensive Comparison with Improved Approximation

This script runs both the original and improved approximation solutions
on all test cases and compares their performance against the exact solution.

It generates:
1. Comparison of original vs improved approximation
2. Identification of test cases where improvement helped
3. Statistical analysis of improvements
"""

import os
import subprocess
import json
import time
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXACT_SCRIPT = os.path.join(PROJECT_ROOT, "exact_solution", "cs412_longestpath_exact.py")
ORIGINAL_APPROX = os.path.join(PROJECT_ROOT, "approx_solution", "cs412_longestpath_approx.py")
IMPROVED_APPROX = os.path.join(PROJECT_ROOT, "part_E", "cs412_longestpath_approx_improved.py")
TEST_DIR = os.path.join(PROJECT_ROOT, "part_E", "part_e_test_cases")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "part_E", "comparison_improved.json")
REPORT_FILE = os.path.join(PROJECT_ROOT, "part_E", "improvement_report.txt")


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


def read_graph_size(test_file):
    """Read number of vertices and edges from test file."""
    try:
        with open(test_file, 'r') as f:
            first_line = f.readline().strip()
            parts = first_line.split()
            if len(parts) >= 2:
                return int(parts[0]), int(parts[1])
    except:
        pass
    return 0, 0


def main():
    """Run comprehensive comparison."""
    if not os.path.exists(TEST_DIR):
        print(f"Error: Test directory {TEST_DIR} not found!")
        print("Please run generate_test_cases.py first.")
        return
    
    # Get all test files
    test_files = sorted([f for f in os.listdir(TEST_DIR) if f.endswith('.txt')])
    
    if not test_files:
        print(f"Error: No test files found in {TEST_DIR}!")
        return
    
    print(f"Found {len(test_files)} test cases")
    print(f"Running comprehensive comparison (this may take a while)...")
    print(f"Comparing: Exact vs Original Approx vs Improved Approx")
    print()
    
    results = []
    improved_count = 0
    same_count = 0
    worse_count = 0
    
    for i, test_file in enumerate(test_files):
        test_path = os.path.join(TEST_DIR, test_file)
        
        if (i + 1) % 100 == 0:
            print(f"Progress: {i + 1}/{len(test_files)} test cases processed...")
        
        n, m = read_graph_size(test_path)
        
        # Run exact solution (with longer timeout for larger graphs)
        exact_timeout = 120 if n <= 10 else 60
        exact_result = run_solution(EXACT_SCRIPT, test_path, timeout=exact_timeout)
        
        # Run original approximation
        original_result = run_solution(ORIGINAL_APPROX, test_path, timeout=30)
        
        # Run improved approximation
        improved_result = run_solution(IMPROVED_APPROX, test_path, timeout=30)
        
        result_entry = {
            'test_file': test_file,
            'vertices': n,
            'edges': m,
            'exact': exact_result,
            'original': original_result,
            'improved': improved_result
        }
        
        # Analyze improvements
        if (exact_result['success'] and original_result['success'] and 
            improved_result['success']):
            exact_len = exact_result['path_length']
            original_len = original_result['path_length']
            improved_len = improved_result['path_length']
            
            if improved_len > original_len:
                improved_count += 1
                result_entry['improvement'] = improved_len - original_len
                result_entry['improvement_pct'] = ((improved_len - original_len) / exact_len * 100) if exact_len > 0 else 0
            elif improved_len == original_len:
                same_count += 1
                result_entry['improvement'] = 0
                result_entry['improvement_pct'] = 0
            else:
                worse_count += 1
                result_entry['improvement'] = improved_len - original_len
                result_entry['improvement_pct'] = 0
            
            # Calculate quality metrics
            result_entry['original_quality'] = (original_len / exact_len * 100) if exact_len > 0 else 0
            result_entry['improved_quality'] = (improved_len / exact_len * 100) if exact_len > 0 else 0
        else:
            result_entry['improvement'] = None
        
        results.append(result_entry)
    
    # Save results
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate report
    with open(REPORT_FILE, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("PART E: IMPROVED APPROXIMATION COMPARISON REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total test cases: {len(test_files)}\n")
        f.write(f"Cases where improved version is better: {improved_count}\n")
        f.write(f"Cases where improved version is same: {same_count}\n")
        f.write(f"Cases where improved version is worse: {worse_count}\n\n")
        
        # Find best improvements
        improvements = [r for r in results if r.get('improvement', 0) > 0]
        if improvements:
            improvements.sort(key=lambda x: x.get('improvement', 0), reverse=True)
            f.write("TOP 20 IMPROVEMENTS\n")
            f.write("-" * 80 + "\n")
            for i, r in enumerate(improvements[:20], 1):
                f.write(f"{i:2d}. {r['test_file']} ({r['vertices']}v, {r['edges']}e)\n")
                f.write(f"    Exact: {r['exact']['path_length']}, ", end="")
                f.write(f"Original: {r['original']['path_length']}, ", end="")
                f.write(f"Improved: {r['improved']['path_length']}\n")
                f.write(f"    Improvement: +{r['improvement']} ({r['improvement_pct']:.2f}%)\n")
                f.write(f"    Quality: {r['original_quality']:.2f}% -> {r['improved_quality']:.2f}%\n\n")
        
        # Cases where improved found optimal but original didn't
        optimal_found = []
        for r in results:
            if (r.get('exact', {}).get('success') and 
                r.get('original', {}).get('success') and
                r.get('improved', {}).get('success')):
                exact_val = r['exact']['path_length']
                orig_val = r['original']['path_length']
                impr_val = r['improved']['path_length']
                if exact_val == impr_val and exact_val != orig_val:
                    optimal_found.append(r)
        
        if optimal_found:
            f.write(f"\nCASES WHERE IMPROVED FOUND OPTIMAL (but original didn't): {len(optimal_found)}\n")
            f.write("-" * 80 + "\n")
            for r in optimal_found[:20]:
                f.write(f"  {r['test_file']} ({r['vertices']}v, {r['edges']}e): ")
                f.write(f"Exact={r['exact']['path_length']}, ", end="")
                f.write(f"Orig={r['original']['path_length']}, ", end="")
                f.write(f"Impr={r['improved']['path_length']}\n")
    
    print()
    print("=" * 60)
    print("COMPARISON COMPLETE!")
    print("=" * 60)
    print(f"Total test cases: {len(test_files)}")
    print(f"Improved version better: {improved_count}")
    print(f"Improved version same: {same_count}")
    print(f"Improved version worse: {worse_count}")
    print()
    print(f"Results saved to: {OUTPUT_FILE}")
    print(f"Report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()

