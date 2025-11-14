#!/usr/bin/env python3
"""
CS 412 Longest Path - Solution Comparison Visualization
This script creates plots comparing exact vs approximation solutions.

References:
- Matplotlib documentation: https://matplotlib.org/stable/contents.html
- NumPy documentation: https://numpy.org/doc/stable/
"""

import os
import sys

# Try to import matplotlib
try:
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib is not installed.")
    print("To install: pip install matplotlib numpy")
    print("Or if using conda: conda install matplotlib numpy")
    print("")
    print("The script will still display the data in text format.")

def read_comparison_data(filename):
    """Read comparison data from file."""
    data = []
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        print("Please run compare_solutions_detailed.sh first.")
        sys.exit(1)
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            parts = line.split('|')
            if len(parts) >= 11:
                try:
                    test_name = parts[0]
                    vertices = int(parts[1])
                    edges = int(parts[2])
                    exact_time = float(parts[3])
                    approx_time = float(parts[4])
                    exact_value = int(parts[5])
                    approx_value = int(parts[6])
                    quality = parts[7]
                    difference = int(parts[8])
                    percent_diff = float(parts[9])
                    speedup_str = parts[10] if len(parts) > 10 else "N/A"
                    speedup = float(speedup_str) if speedup_str != "N/A" else None
                    
                    data.append({
                        'test_name': test_name,
                        'vertices': vertices,
                        'edges': edges,
                        'exact_time': exact_time,
                        'approx_time': approx_time,
                        'exact_value': exact_value,
                        'approx_value': approx_value,
                        'quality': quality,
                        'difference': difference,
                        'percent_diff': percent_diff,
                        'speedup': speedup
                    })
                except (ValueError, IndexError):
                    continue
    
    return data

def plot_comparison(data):
    """Create comparison plots."""
    if not HAS_MATPLOTLIB:
        # Print text summary
        print("Comparison Data Summary:")
        print("=" * 100)
        print(f"{'Test':<20} {'Vertices':<10} {'Exact Time':<12} {'Approx Time':<12} {'Exact Val':<10} {'Approx Val':<10} {'Quality':<12} {'Speedup':<10}")
        print("-" * 100)
        for d in data:
            speedup_str = f"{d['speedup']:.2f}x" if d['speedup'] else "N/A"
            print(f"{d['test_name']:<20} {d['vertices']:<10} {d['exact_time']:<12.6f} {d['approx_time']:<12.6f} {d['exact_value']:<10} {d['approx_value']:<10} {d['quality']:<12} {speedup_str:<10}")
        print("=" * 100)
        return
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Exact vs Approximation Solution Comparison', fontsize=16, fontweight='bold')
    
    # Extract data
    vertices = [d['vertices'] for d in data]
    exact_times = [d['exact_time'] for d in data]
    approx_times = [d['approx_time'] for d in data]
    exact_values = [d['exact_value'] for d in data]
    approx_values = [d['approx_value'] for d in data]
    speedups = [d['speedup'] for d in data if d['speedup']]
    
    # Plot 1: Runtime Comparison
    ax1 = axes[0, 0]
    x = np.arange(len(data))
    width = 0.35
    
    ax1.bar(x - width/2, exact_times, width, label='Exact', color='red', alpha=0.7)
    ax1.bar(x + width/2, approx_times, width, label='Approximation', color='green', alpha=0.7)
    ax1.set_xlabel('Test Case', fontsize=12)
    ax1.set_ylabel('Runtime (seconds)', fontsize=12)
    ax1.set_title('Runtime Comparison', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([d['test_name'][:10] for d in data], rotation=45, ha='right')
    ax1.set_yscale('log')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Solution Quality Comparison
    ax2 = axes[0, 1]
    ax2.plot(vertices, exact_values, 'ro-', label='Exact (Optimal)', linewidth=2, markersize=8)
    ax2.plot(vertices, approx_values, 'gs-', label='Approximation', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Vertices', fontsize=12)
    ax2.set_ylabel('Path Length', fontsize=12)
    ax2.set_title('Solution Quality Comparison', fontsize=13, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Speedup Factor
    ax3 = axes[1, 0]
    if speedups:
        valid_indices = [i for i, d in enumerate(data) if d['speedup']]
        valid_vertices = [vertices[i] for i in valid_indices]
        valid_speedups = [speedups[i] for i in range(len(speedups))]
        
        ax3.bar(range(len(valid_speedups)), valid_speedups, color='blue', alpha=0.7)
        ax3.set_xlabel('Test Case', fontsize=12)
        ax3.set_ylabel('Speedup Factor (x)', fontsize=12)
        ax3.set_title('Approximation Speedup vs Exact', fontsize=13, fontweight='bold')
        ax3.set_xticks(range(len(valid_indices)))
        ax3.set_xticklabels([data[i]['test_name'][:10] for i in valid_indices], rotation=45, ha='right')
        ax3.grid(True, alpha=0.3, axis='y')
        ax3.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='1x (no speedup)')
        ax3.legend()
    else:
        ax3.text(0.5, 0.5, 'No speedup data available', 
                ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title('Approximation Speedup vs Exact', fontsize=13, fontweight='bold')
    
    # Plot 4: Quality Analysis Table
    ax4 = axes[1, 1]
    ax4.axis('tight')
    ax4.axis('off')
    
    table_data = []
    headers = ['Test', 'Exact', 'Approx', 'Diff', '% Diff', 'Quality']
    
    for d in data:
        diff_str = str(d['difference'])
        percent_str = f"{d['percent_diff']:.2f}%" if d['percent_diff'] > 0 else "0%"
        quality_color = 'green' if d['quality'] == 'OPTIMAL' else 'yellow'
        table_data.append([
            d['test_name'][:12],
            str(d['exact_value']),
            str(d['approx_value']),
            diff_str,
            percent_str,
            d['quality']
        ])
    
    table = ax4.table(cellText=table_data, colLabels=headers,
                     cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    
    # Color code quality
    for i, d in enumerate(data):
        if d['quality'] == 'OPTIMAL':
            for j in range(6):
                table[(i+1, j)].set_facecolor('#ccffcc')
        else:
            for j in range(6):
                table[(i+1, j)].set_facecolor('#ffffcc')
    
    ax4.set_title('Solution Quality Analysis', fontsize=13, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    # Save plots
    output_png = os.path.join(os.path.dirname(__file__), 'solution_comparison.png')
    output_pdf = os.path.join(os.path.dirname(__file__), 'solution_comparison.pdf')
    
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    plt.savefig(output_pdf, bbox_inches='tight')
    
    print(f"Comparison plots saved to:")
    print(f"  - {output_png}")
    print(f"  - {output_pdf}")
    
    plt.show()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, 'comparison_data.txt')
    
    print("Reading comparison data...")
    data = read_comparison_data(data_file)
    
    if not data:
        print("No data found. Please run compare_solutions_detailed.sh first.")
        return
    
    print(f"Found {len(data)} test cases")
    print("Generating plots...")
    plot_comparison(data)
    print("Done!")

if __name__ == "__main__":
    main()

