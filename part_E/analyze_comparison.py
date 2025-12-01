#!/usr/bin/env python3
"""
Analysis Script for Comparison Results
Generates comprehensive analysis report comparing exact vs approximation solutions.
"""

import json
import os
from collections import defaultdict
import statistics

def load_results(filename):
    """Load comparison results from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def analyze_results(results):
    """Analyze comparison results and generate statistics."""
    analysis = {
        'total': len(results),
        'exact_failures': 0,
        'approx_failures': 0,
        'matches': 0,
        'mismatches': 0,
        'mismatch_details': [],
        'statistics': {}
    }
    
    differences = []
    ratios = []
    exact_times = []
    approx_times = []
    
    for result in results:
        exact = result['exact']
        approx = result['approx']
        
        if not exact['success']:
            analysis['exact_failures'] += 1
        if not approx['success']:
            analysis['approx_failures'] += 1
        
        if exact['success'] and approx['success']:
            exact_times.append(exact['time'])
            approx_times.append(approx['time'])
            
            if result.get('match', False):
                analysis['matches'] += 1
            else:
                analysis['mismatches'] += 1
                diff = result.get('difference', 0)
                ratio = result.get('ratio', 0.0)
                differences.append(diff)
                ratios.append(ratio)
                
                analysis['mismatch_details'].append({
                    'test_file': result['test_file'],
                    'exact_length': exact['path_length'],
                    'approx_length': approx['path_length'],
                    'difference': diff,
                    'ratio': ratio,
                    'exact_time': exact['time'],
                    'approx_time': approx['time']
                })
    
    # Calculate statistics
    if differences:
        analysis['statistics']['differences'] = {
            'min': min(differences),
            'max': max(differences),
            'mean': statistics.mean(differences),
            'median': statistics.median(differences),
            'stdev': statistics.stdev(differences) if len(differences) > 1 else 0
        }
    
    if ratios:
        analysis['statistics']['ratios'] = {
            'min': min(ratios),
            'max': max(ratios),
            'mean': statistics.mean(ratios),
            'median': statistics.median(ratios),
            'stdev': statistics.stdev(ratios) if len(ratios) > 1 else 0
        }
    
    if exact_times:
        analysis['statistics']['exact_times'] = {
            'min': min(exact_times),
            'max': max(exact_times),
            'mean': statistics.mean(exact_times),
            'median': statistics.median(exact_times),
            'total': sum(exact_times)
        }
    
    if approx_times:
        analysis['statistics']['approx_times'] = {
            'min': min(approx_times),
            'max': max(approx_times),
            'mean': statistics.mean(approx_times),
            'median': statistics.median(approx_times),
            'total': sum(approx_times)
        }
    
    return analysis

def generate_report(analysis, output_file):
    """Generate a comprehensive text report."""
    with open(output_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("COMPREHENSIVE COMPARISON: EXACT vs APPROXIMATION SOLUTIONS\n")
        f.write("=" * 80 + "\n\n")
        
        # Summary
        f.write("EXECUTIVE SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total test cases: {analysis['total']}\n")
        f.write(f"Exact solution failures: {analysis['exact_failures']}\n")
        f.write(f"Approximation solution failures: {analysis['approx_failures']}\n")
        f.write(f"Cases where results match: {analysis['matches']}\n")
        f.write(f"Cases where results differ: {analysis['mismatches']}\n")
        f.write(f"Match rate: {analysis['matches'] / (analysis['matches'] + analysis['mismatches']) * 100:.2f}%\n")
        f.write(f"Approximation accuracy (cases where it finds optimal): {analysis['matches'] / (analysis['matches'] + analysis['mismatches']) * 100:.2f}%\n")
        f.write("\n")
        
        # Statistics
        if analysis['statistics']:
            f.write("STATISTICAL ANALYSIS\n")
            f.write("-" * 80 + "\n")
            
            if 'differences' in analysis['statistics']:
                stats = analysis['statistics']['differences']
                f.write("\nPath Length Differences (Exact - Approximation):\n")
                f.write(f"  Minimum difference: {stats['min']}\n")
                f.write(f"  Maximum difference: {stats['max']}\n")
                f.write(f"  Mean difference: {stats['mean']:.2f}\n")
                f.write(f"  Median difference: {stats['median']:.2f}\n")
                f.write(f"  Standard deviation: {stats['stdev']:.2f}\n")
            
            if 'ratios' in analysis['statistics']:
                stats = analysis['statistics']['ratios']
                f.write("\nApproximation Ratio (Approx / Exact):\n")
                f.write(f"  Minimum ratio: {stats['min']:.4f} ({stats['min']*100:.2f}%)\n")
                f.write(f"  Maximum ratio: {stats['max']:.4f} ({stats['max']*100:.2f}%)\n")
                f.write(f"  Mean ratio: {stats['mean']:.4f} ({stats['mean']*100:.2f}%)\n")
                f.write(f"  Median ratio: {stats['median']:.4f} ({stats['median']*100:.2f}%)\n")
                f.write(f"  Standard deviation: {stats['stdev']:.4f}\n")
            
            if 'exact_times' in analysis['statistics']:
                stats = analysis['statistics']['exact_times']
                f.write("\nExact Solution Runtime:\n")
                f.write(f"  Minimum time: {stats['min']:.4f} seconds\n")
                f.write(f"  Maximum time: {stats['max']:.4f} seconds\n")
                f.write(f"  Mean time: {stats['mean']:.4f} seconds\n")
                f.write(f"  Median time: {stats['median']:.4f} seconds\n")
                f.write(f"  Total time: {stats['total']:.2f} seconds\n")
            
            if 'approx_times' in analysis['statistics']:
                stats = analysis['statistics']['approx_times']
                f.write("\nApproximation Solution Runtime:\n")
                f.write(f"  Minimum time: {stats['min']:.4f} seconds\n")
                f.write(f"  Maximum time: {stats['max']:.4f} seconds\n")
                f.write(f"  Mean time: {stats['mean']:.4f} seconds\n")
                f.write(f"  Median time: {stats['median']:.4f} seconds\n")
                f.write(f"  Total time: {stats['total']:.2f} seconds\n")
            
            if 'exact_times' in analysis['statistics'] and 'approx_times' in analysis['statistics']:
                speedup = analysis['statistics']['exact_times']['total'] / analysis['statistics']['approx_times']['total']
                f.write(f"\nSpeedup (Exact / Approximation): {speedup:.2f}x\n")
        
        f.write("\n")
        
        # Worst cases
        if analysis['mismatch_details']:
            f.write("WORST APPROXIMATION CASES (Largest Differences)\n")
            f.write("-" * 80 + "\n")
            sorted_by_diff = sorted(analysis['mismatch_details'], 
                                   key=lambda x: x['difference'], reverse=True)
            
            f.write("\nTop 50 cases with largest differences:\n\n")
            for i, case in enumerate(sorted_by_diff[:50], 1):
                f.write(f"{i:3d}. {case['test_file']}\n")
                f.write(f"     Exact: {case['exact_length']}, Approximation: {case['approx_length']}\n")
                f.write(f"     Difference: {case['difference']}, Ratio: {case['ratio']:.4f} ({case['ratio']*100:.2f}%)\n")
                f.write(f"     Exact time: {case['exact_time']:.4f}s, Approx time: {case['approx_time']:.4f}s\n")
                f.write("\n")
            
            # Cases where approximation is significantly worse
            f.write("\nCASES WHERE APPROXIMATION IS < 80% OF OPTIMAL\n")
            f.write("-" * 80 + "\n")
            poor_cases = [c for c in sorted_by_diff if c['ratio'] < 0.8]
            f.write(f"Found {len(poor_cases)} cases where approximation is less than 80% of optimal:\n\n")
            for i, case in enumerate(poor_cases[:100], 1):
                f.write(f"{i:3d}. {case['test_file']}: {case['ratio']*100:.2f}% (diff: {case['difference']})\n")
        
        f.write("\n")
        f.write("=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")

def main():
    """Main analysis function."""
    results_file = "part_e_comparison_results.json"
    report_file = "part_e_comparison_report.txt"
    
    if not os.path.exists(results_file):
        print(f"Error: Results file {results_file} not found!")
        print("Please run run_comparison.py first.")
        return
    
    print("Loading results...")
    results = load_results(results_file)
    
    print("Analyzing results...")
    analysis = analyze_results(results)
    
    print("Generating report...")
    generate_report(analysis, report_file)
    
    print(f"\nAnalysis complete!")
    print(f"Report saved to: {report_file}")
    print(f"\nSummary:")
    print(f"  Total cases: {analysis['total']}")
    print(f"  Matches: {analysis['matches']}")
    print(f"  Mismatches: {analysis['mismatches']}")
    if analysis['mismatches'] > 0:
        print(f"  Match rate: {analysis['matches'] / (analysis['matches'] + analysis['mismatches']) * 100:.2f}%")
        if 'ratios' in analysis['statistics']:
            print(f"  Mean approximation ratio: {analysis['statistics']['ratios']['mean']:.4f} ({analysis['statistics']['ratios']['mean']*100:.2f}%)")

if __name__ == "__main__":
    main()

