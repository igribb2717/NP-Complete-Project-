#!/usr/bin/env python3
"""
Approximation Error Percentage Analysis

This script analyzes the non-averaged run data to calculate how well the
approximation algorithm performs compared to the exact (optimal) solution.

ERROR METRIC:
-------------
Error Percentage = (Approximate Solution Value / Exact Solution Value) * 100

- 100% = Perfect (approximation found optimal solution)
- < 100% = Suboptimal (approximation is worse than optimal)
- Lower percentages indicate worse performance

This metric helps identify:
1. Which test sizes are most challenging for the approximation
2. Overall approximation quality
3. Areas where the algorithm needs improvement

OUTPUT:
-------
- error_analysis_report.txt: Detailed text report with all statistics
- error_analysis_summary.txt: Quick summary for quick reference

USAGE:
------
Run this after generating comparison_runs_part_D.txt:
  python3 part_D/analyze_error_percentage.py

Then review the reports to identify:
- Test cases where approximation performs poorly
- Graph sizes (vertices/edges) that are problematic
- Overall approximation quality to guide algorithm improvements
"""

import os
import sys
from collections import defaultdict

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNS_FILE = os.path.join(PROJECT_ROOT, "part_D", "comparison_runs_part_D.txt")
AVG_DATA_FILE = os.path.join(PROJECT_ROOT, "part_D", "comparison_data_part_D.txt")
REPORT_FILE = os.path.join(PROJECT_ROOT, "part_D", "error_analysis_report.txt")
SUMMARY_FILE = os.path.join(PROJECT_ROOT, "part_D", "error_analysis_summary.txt")


def read_test_sizes():
    """Read test case sizes (vertices, edges) from averaged data file."""
    sizes = {}
    if not os.path.exists(AVG_DATA_FILE):
        return sizes
    
    with open(AVG_DATA_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('|')
            if len(parts) >= 3:
                try:
                    test_name = parts[0]
                    vertices = int(parts[1])
                    edges = int(parts[2])
                    sizes[test_name] = (vertices, edges)
                except (ValueError, IndexError):
                    continue
    return sizes


def read_run_data():
    """Read all individual runs from comparison_runs_part_D.txt."""
    if not os.path.exists(RUNS_FILE):
        print(f"Error: {RUNS_FILE} not found!")
        print("Please run: python3 part_D/run_part_D_runtime_study.py first")
        sys.exit(1)
    
    # Structure: test_name -> solver -> list of (run_id, runtime, path_length)
    runs = defaultdict(lambda: defaultdict(list))
    
    with open(RUNS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('|')
            if len(parts) >= 5:
                try:
                    test_name = parts[0]
                    solver = parts[1]  # 'exact' or 'approx'
                    run_id = parts[2]
                    runtime = float(parts[3])
                    path_length = int(parts[4])
                    runs[test_name][solver].append((run_id, runtime, path_length))
                except (ValueError, IndexError):
                    continue
    
    return runs


def calculate_error_percentages(runs, test_sizes):
    """
    Calculate error percentages for each test case.
    
    Returns:
        List of dicts with: test_name, vertices, edges, error_pcts (list), avg_error, min_error, max_error
    """
    results = []
    
    for test_name in sorted(runs.keys()):
        if 'exact' not in runs[test_name] or 'approx' not in runs[test_name]:
            continue
        
        exact_runs = runs[test_name]['exact']
        approx_runs = runs[test_name]['approx']
        
        # Get test size
        vertices, edges = test_sizes.get(test_name, (0, 0))
        
        # Calculate error % for each run pair
        # We'll match runs by index (run_1 with run_1, etc.)
        error_percentages = []
        
        # Get exact values (should be consistent across runs)
        exact_values = [pl for _, _, pl in exact_runs]
        approx_values = [pl for _, _, pl in approx_runs]
        
        # Use average exact value (should be same, but average for safety)
        avg_exact = sum(exact_values) / len(exact_values) if exact_values else 0
        
        if avg_exact == 0:
            continue  # Skip if no valid exact solution
        
        # Calculate error % for each approx run
        for approx_val in approx_values:
            error_pct = (approx_val / avg_exact) * 100.0
            error_percentages.append(error_pct)
        
        if not error_percentages:
            continue
        
        results.append({
            'test_name': test_name,
            'vertices': vertices,
            'edges': edges,
            'exact_value': int(avg_exact),
            'error_percentages': error_percentages,
            'avg_error': sum(error_percentages) / len(error_percentages),
            'min_error': min(error_percentages),
            'max_error': max(error_percentages),
            'num_runs': len(error_percentages)
        })
    
    return results


def group_by_size(results):
    """Group results by test size (vertices, edges)."""
    by_size = defaultdict(list)
    
    for result in results:
        key = (result['vertices'], result['edges'])
        by_size[key].append(result)
    
    return by_size


def calculate_size_statistics(by_size):
    """Calculate average error % for each test size."""
    size_stats = []
    
    for (vertices, edges), test_results in sorted(by_size.items()):
        all_errors = []
        for result in test_results:
            all_errors.extend(result['error_percentages'])
        
        if not all_errors:
            continue
        
        size_stats.append({
            'vertices': vertices,
            'edges': edges,
            'num_tests': len(test_results),
            'num_runs': len(all_errors),
            'avg_error': sum(all_errors) / len(all_errors),
            'min_error': min(all_errors),
            'max_error': max(all_errors),
            'std_dev': calculate_std_dev(all_errors) if len(all_errors) > 1 else 0.0
        })
    
    return size_stats


def calculate_std_dev(values):
    """Calculate standard deviation."""
    if len(values) <= 1:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    return variance ** 0.5


def generate_report(results, size_stats):
    """Generate detailed error analysis report."""
    all_errors = []
    for result in results:
        all_errors.extend(result['error_percentages'])
    
    overall_avg = sum(all_errors) / len(all_errors) if all_errors else 0
    overall_min = min(all_errors) if all_errors else 0
    overall_max = max(all_errors) if all_errors else 0
    
    with open(REPORT_FILE, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("APPROXIMATION ERROR PERCENTAGE ANALYSIS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("METRIC EXPLANATION:\n")
        f.write("-" * 80 + "\n")
        f.write("Error Percentage = (Approximate Value / Exact Value) * 100\n\n")
        f.write("Interpretation:\n")
        f.write("  - 100.00% = Perfect (approximation found optimal solution)\n")
        f.write("  - 95.00%  = Approximation is 5% worse than optimal\n")
        f.write("  - 90.00%  = Approximation is 10% worse than optimal\n")
        f.write("  - < 90%   = Poor performance (needs algorithm improvement)\n\n")
        f.write("This metric helps identify:\n")
        f.write("  1. Which test sizes are most challenging\n")
        f.write("  2. Overall approximation quality\n")
        f.write("  3. Areas where the algorithm needs improvement\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("OVERALL STATISTICS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total test cases analyzed: {len(results)}\n")
        f.write(f"Total individual runs: {len(all_errors)}\n")
        f.write(f"\nOverall Error Percentage:\n")
        f.write(f"  Average: {overall_avg:.2f}%\n")
        f.write(f"  Minimum: {overall_min:.2f}%\n")
        f.write(f"  Maximum: {overall_max:.2f}%\n")
        if len(all_errors) > 1:
            std_dev = calculate_std_dev(all_errors)
            f.write(f"  Standard Deviation: {std_dev:.2f}%\n")
        f.write(f"\n")
        
        # Count optimal vs suboptimal
        optimal_count = sum(1 for e in all_errors if abs(e - 100.0) < 0.01)
        suboptimal_count = len(all_errors) - optimal_count
        f.write(f"Runs finding optimal solution: {optimal_count} ({optimal_count/len(all_errors)*100:.1f}%)\n")
        f.write(f"Runs finding suboptimal solution: {suboptimal_count} ({suboptimal_count/len(all_errors)*100:.1f}%)\n\n")
        
        f.write("=" * 80 + "\n")
        f.write("STATISTICS BY TEST SIZE\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"{'Vertices':<10} {'Edges':<10} {'Tests':<8} {'Runs':<8} "
                f"{'Avg Error %':<12} {'Min %':<10} {'Max %':<10} {'Std Dev':<10}\n")
        f.write("-" * 80 + "\n")
        
        for stat in size_stats:
            f.write(f"{stat['vertices']:<10} {stat['edges']:<10} {stat['num_tests']:<8} "
                    f"{stat['num_runs']:<8} {stat['avg_error']:<12.2f} "
                    f"{stat['min_error']:<10.2f} {stat['max_error']:<10.2f} "
                    f"{stat['std_dev']:<10.2f}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("DETAILED RESULTS BY TEST CASE\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"{'Test Name':<25} {'Vertices':<10} {'Edges':<10} {'Exact':<8} "
                f"{'Avg Error %':<12} {'Min %':<10} {'Max %':<10} {'Runs':<6}\n")
        f.write("-" * 80 + "\n")
        
        for result in sorted(results, key=lambda x: (x['vertices'], x['edges'], x['test_name'])):
            f.write(f"{result['test_name']:<25} {result['vertices']:<10} {result['edges']:<10} "
                    f"{result['exact_value']:<8} {result['avg_error']:<12.2f} "
                    f"{result['min_error']:<10.2f} {result['max_error']:<10.2f} "
                    f"{result['num_runs']:<6}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("RECOMMENDATIONS FOR ALGORITHM IMPROVEMENT\n")
        f.write("=" * 80 + "\n\n")
        
        # Find worst performing test sizes
        worst_sizes = sorted(size_stats, key=lambda x: x['avg_error'])[:3]
        f.write("Test sizes with worst approximation performance:\n")
        for stat in worst_sizes:
            f.write(f"  - {stat['vertices']} vertices, {stat['edges']} edges: "
                    f"avg {stat['avg_error']:.2f}% (target: improve to >95%)\n")
        
        f.write("\nTest cases with worst individual performance:\n")
        worst_tests = sorted(results, key=lambda x: x['avg_error'])[:5]
        for result in worst_tests:
            if result['avg_error'] < 100.0:
                f.write(f"  - {result['test_name']} ({result['vertices']}v, {result['edges']}e): "
                        f"avg {result['avg_error']:.2f}% (exact={result['exact_value']})\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")
    
    print(f"Detailed report written to: {REPORT_FILE}")


def generate_summary(results, size_stats):
    """Generate quick summary file."""
    all_errors = []
    for result in results:
        all_errors.extend(result['error_percentages'])
    
    overall_avg = sum(all_errors) / len(all_errors) if all_errors else 0
    optimal_count = sum(1 for e in all_errors if abs(e - 100.0) < 0.01)
    
    with open(SUMMARY_FILE, 'w') as f:
        f.write("APPROXIMATION ERROR PERCENTAGE - QUICK SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Overall Average Error: {overall_avg:.2f}%\n")
        f.write(f"Optimal Solutions Found: {optimal_count}/{len(all_errors)} "
                f"({optimal_count/len(all_errors)*100:.1f}%)\n\n")
        f.write("By Test Size:\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Vertices':<10} {'Edges':<10} {'Avg Error %':<15}\n")
        f.write("-" * 60 + "\n")
        for stat in sorted(size_stats, key=lambda x: (x['vertices'], x['edges'])):
            f.write(f"{stat['vertices']:<10} {stat['edges']:<10} {stat['avg_error']:<15.2f}\n")
    
    print(f"Summary written to: {SUMMARY_FILE}")


def main():
    print("Reading test case sizes...")
    test_sizes = read_test_sizes()
    
    print("Reading individual run data...")
    runs = read_run_data()
    
    print("Calculating error percentages...")
    results = calculate_error_percentages(runs, test_sizes)
    
    if not results:
        print("Error: No valid results found!")
        return
    
    print("Grouping by test size...")
    by_size = group_by_size(results)
    
    print("Calculating statistics by size...")
    size_stats = calculate_size_statistics(by_size)
    
    print("Generating reports...")
    generate_report(results, size_stats)
    generate_summary(results, size_stats)
    
    print("\nAnalysis complete!")
    print(f"\nView results:")
    print(f"  - Detailed report: {REPORT_FILE}")
    print(f"  - Quick summary: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()


