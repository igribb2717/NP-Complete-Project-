#!/usr/bin/env python3
"""
CS 412 Longest Path - Runtime Visualization
This script reads runtime data and creates plots showing how runtime varies with input size.

References:
- Matplotlib documentation: https://matplotlib.org/stable/contents.html
- NumPy documentation: https://numpy.org/doc/stable/
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def read_runtime_data(filename):
    """
    Read runtime data from the measurement output file.
    
    Returns:
        List of tuples: (test_name, vertices, edges, runtime_seconds)
    """
    data = []
    
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        print("Please run measure_runtime.sh first to generate runtime data.")
        sys.exit(1)
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) >= 4:
                test_name = parts[0]
                try:
                    vertices = int(parts[1])
                    edges = int(parts[2])
                    runtime = float(parts[3]) if parts[3] != "ERROR" else None
                    data.append((test_name, vertices, edges, runtime))
                except ValueError:
                    continue
    
    return data

def plot_runtime_analysis(data):
    """
    Create plots showing runtime vs input size.
    """
    # Filter out errors
    valid_data = [(name, v, e, r) for name, v, e, r in data if r is not None]
    
    if not valid_data:
        print("No valid runtime data to plot.")
        return
    
    # Extract data
    test_names = [d[0] for d in valid_data]
    vertices = [d[1] for d in valid_data]
    edges = [d[2] for d in valid_data]
    runtimes = [d[3] for d in valid_data]
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Longest Path Exact Solution - Runtime Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Runtime vs Number of Vertices
    ax1 = axes[0, 0]
    ax1.plot(vertices, runtimes, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('Number of Vertices (n)', fontsize=12)
    ax1.set_ylabel('Runtime (seconds)', fontsize=12)
    ax1.set_title('Runtime vs Number of Vertices', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')  # Log scale for better visualization
    
    # Add annotations for large test cases
    for i, (v, r, name) in enumerate(zip(vertices, runtimes, test_names)):
        if r > 60 or 'large' in name.lower() or 'extreme' in name.lower():
            ax1.annotate(f'n={v}', (v, r), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontsize=8)
    
    # Plot 2: Runtime vs Number of Edges
    ax2 = axes[0, 1]
    ax2.plot(edges, runtimes, 'ro-', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Edges (m)', fontsize=12)
    ax2.set_ylabel('Runtime (seconds)', fontsize=12)
    ax2.set_title('Runtime vs Number of Edges', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale('log')
    
    # Plot 3: Runtime vs n (with exponential fit visualization)
    ax3 = axes[1, 0]
    ax3.plot(vertices, runtimes, 'go-', linewidth=2, markersize=8, label='Actual Runtime')
    ax3.set_xlabel('Number of Vertices (n)', fontsize=12)
    ax3.set_ylabel('Runtime (seconds)', fontsize=12)
    ax3.set_title('Runtime Growth (Log-Log Scale)', fontsize=13, fontweight='bold')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.grid(True, alpha=0.3)
    
    # Add theoretical O(n!) reference line (scaled)
    if len(vertices) > 2:
        x_theory = np.array(vertices)
        # Scale factor to roughly match the data
        scale_factor = runtimes[-1] / (np.math.factorial(vertices[-1]) if vertices[-1] <= 10 else 1e10)
        y_theory = [scale_factor * np.math.factorial(v) if v <= 10 else scale_factor * 1e10 for v in x_theory]
        ax3.plot(x_theory, y_theory, 'r--', linewidth=1, alpha=0.5, label='O(n!) reference (scaled)')
        ax3.legend()
    
    # Plot 4: Table of results
    ax4 = axes[1, 1]
    ax4.axis('tight')
    ax4.axis('off')
    
    # Create table data
    table_data = []
    headers = ['Test Case', 'n', 'm', 'Time (s)']
    
    for name, v, e, r in valid_data:
        time_str = f"{r:.4f}" if r < 1000 else f"{r:.1f}"
        # Truncate long names
        short_name = name.replace('test_input_', '')[:15]
        table_data.append([short_name, str(v), str(e), time_str])
    
    table = ax4.table(cellText=table_data, colLabels=headers, 
                     cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    
    # Highlight rows with runtime > 60 seconds
    for i, (_, _, _, r) in enumerate(valid_data):
        if r > 60:
            for j in range(4):
                table[(i+1, j)].set_facecolor('#ffcccc')
    
    ax4.set_title('Runtime Summary Table', fontsize=13, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    # Save plot
    output_file = os.path.join(os.path.dirname(__file__), 'runtime_analysis.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Runtime analysis plot saved to: {output_file}")
    
    # Also save as PDF
    output_file_pdf = os.path.join(os.path.dirname(__file__), 'runtime_analysis.pdf')
    plt.savefig(output_file_pdf, bbox_inches='tight')
    print(f"Runtime analysis plot (PDF) saved to: {output_file_pdf}")
    
    plt.show()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, 'runtime_data.txt')
    
    print("Reading runtime data...")
    data = read_runtime_data(data_file)
    
    if not data:
        print("No data found. Please run measure_runtime.sh first.")
        return
    
    print(f"Found {len(data)} test cases")
    print("Generating plots...")
    plot_runtime_analysis(data)
    print("Done!")

if __name__ == "__main__":
    main()

