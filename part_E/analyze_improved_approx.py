#!/usr/bin/env python3
"""
Analyze the improved approximation solution (cs412_longestpath_approx_improved.py)
against all test cases and generate performance statistics.
"""

import os
import subprocess
import csv
import sys
import json
import statistics

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
        print(f"Error running {script_path} on {test_file}: {e}", file=sys.stderr)
        return None

def main():
    """Main analysis function."""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    test_dir = os.path.join(script_dir, "part_e_test_cases")
    exact_script = os.path.join(project_root, "exact_solution", "cs412_longestpath_exact.py")
    improved_approx_script = os.path.join(script_dir, "cs412_longestpath_approx_improved.py")
    
    if not os.path.exists(test_dir):
        print(f"Error: Test directory {test_dir} not found!")
        return
    
    if not os.path.exists(exact_script):
        print(f"Error: Exact solution script {exact_script} not found!")
        return
    
    if not os.path.exists(improved_approx_script):
        print(f"Error: Improved approximation script {improved_approx_script} not found!")
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
    specific_test_cases = ['test_1026.txt', 'test_0895.txt', 'test_0931.txt', 'test_0936.txt', 'test_0941.txt']
    specific_results = []
    
    for i, test_file in enumerate(test_files):
        test_path = os.path.join(test_dir, test_file)
        
        if (i + 1) % 100 == 0:
            print(f"Progress: {i + 1}/{len(test_files)} test cases processed...")
        
        # Run improved approximation solution
        improved_length = run_solution(improved_approx_script, test_path, timeout=30)
        
        # Run exact solution
        exact_length = run_solution(exact_script, test_path, timeout=120)
        
        if improved_length is not None and exact_length is not None:
            ratio = improved_length / exact_length if exact_length > 0 else 0.0
            percentage = ratio * 100
            difference = exact_length - improved_length
            
            result_entry = {
                'test_file': test_file,
                'improved_length': improved_length,
                'exact_length': exact_length,
                'ratio': ratio,
                'percentage': percentage,
                'difference': difference
            }
            
            results.append(result_entry)
            
            # Store results for specific test cases
            if test_file in specific_test_cases:
                specific_results.append(result_entry)
        elif improved_length is None:
            print(f"Warning: Improved approximation failed on {test_file}", file=sys.stderr)
        elif exact_length is None:
            print(f"Warning: Exact solution failed on {test_file}", file=sys.stderr)
    
    print(f"\nSuccessfully processed {len(results)} test cases")
    
    # Calculate statistics
    if results:
        ratios = [r['ratio'] for r in results]
        percentages = [r['percentage'] for r in results]
        differences = [r['difference'] for r in results]
        
        matches = sum(1 for r in results if r['ratio'] == 1.0)
        optimal_count = matches
        
        print("\n" + "=" * 80)
        print("IMPROVED APPROXIMATION PERFORMANCE ANALYSIS")
        print("=" * 80)
        print(f"Total test cases analyzed: {len(results)}")
        print(f"Cases where improved approximation found optimal: {optimal_count} ({optimal_count/len(results)*100:.2f}%)")
        print(f"\nPerformance Statistics (as percentage of optimal):")
        print(f"  Minimum: {min(percentages):.2f}%")
        print(f"  Maximum: {max(percentages):.2f}%")
        print(f"  Mean: {statistics.mean(percentages):.2f}%")
        print(f"  Median: {statistics.median(percentages):.2f}%")
        if len(percentages) > 1:
            print(f"  Standard Deviation: {statistics.stdev(percentages):.2f}%")
        
        print(f"\nDifference Statistics (Exact - Improved):")
        print(f"  Minimum difference: {min(differences)}")
        print(f"  Maximum difference: {max(differences)}")
        print(f"  Mean difference: {statistics.mean(differences):.2f}")
        print(f"  Median difference: {statistics.median(differences):.2f}")
        if len(differences) > 1:
            print(f"  Standard Deviation: {statistics.stdev(differences):.2f}")
        
        # Performance buckets
        perfect = sum(1 for p in percentages if p == 100.0)
        excellent = sum(1 for p in percentages if 90.0 <= p < 100.0)
        good = sum(1 for p in percentages if 80.0 <= p < 90.0)
        fair = sum(1 for p in percentages if 70.0 <= p < 80.0)
        poor = sum(1 for p in percentages if p < 70.0)
        
        print(f"\nPerformance Distribution:")
        print(f"  100% (Optimal): {perfect} cases ({perfect/len(results)*100:.2f}%)")
        print(f"  90-99%: {excellent} cases ({excellent/len(results)*100:.2f}%)")
        print(f"  80-89%: {good} cases ({good/len(results)*100:.2f}%)")
        print(f"  70-79%: {fair} cases ({fair/len(results)*100:.2f}%)")
        print(f"  <70%: {poor} cases ({poor/len(results)*100:.2f}%)")
    
    # Write CSV for specific test cases (1026, 895, 931, 936, 941)
    if specific_results:
        # Sort by test file name to match the order requested
        specific_results.sort(key=lambda x: x['test_file'])
        
        csv_file = os.path.join(script_dir, "improved_approx_specific_cases.csv")
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Test File', 'Improved Approximation Length', 'Exact Length', 'Percentage of Optimal', 'Difference'])
            for case in specific_results:
                writer.writerow([
                    case['test_file'],
                    case['improved_length'],
                    case['exact_length'],
                    f"{case['percentage']:.2f}%",
                    case['difference']
                ])
        
        print(f"\nCreated CSV file: {csv_file}")
        print("\nResults for specific test cases:")
        print("-" * 80)
        for case in specific_results:
            print(f"{case['test_file']}: Improved={case['improved_length']}, Exact={case['exact_length']}, "
                  f"Percentage={case['percentage']:.2f}%, Difference={case['difference']}")
    else:
        print("\nWarning: Could not find results for all requested specific test cases")
        print(f"Found: {[r['test_file'] for r in specific_results]}")
        print(f"Requested: {specific_test_cases}")
    
    # Save full results to JSON for future reference
    json_file = os.path.join(script_dir, "improved_approx_full_results.json")
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nFull results saved to: {json_file}")
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()

