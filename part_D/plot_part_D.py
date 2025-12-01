#!/usr/bin/env python3
"""
Part D: Runtime and Solution Quality Plots

This script reads the detailed comparison data produced by
`compare_solutions_detailed.sh` (stored in `comparison_data.txt`
at the project root) and generates:

- A runtime comparison plot (exact vs approximation)
- A solution-quality comparison plot (exact value vs approx value)

Outputs are written into the `part_D` folder as PNG and PDF files.
"""

import os
import sys

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Error: matplotlib is not installed.")
    print("Install with one of the following commands:")
    print("  pip install matplotlib")
    print("  # or")
    print("  conda install matplotlib")
    sys.exit(1)


def read_comparison_data(path):
    """Read comparison data into a list of dicts."""
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        print("Make sure you run `bash compare_solutions_detailed.sh` "
              "from the project root first.")
        sys.exit(1)

    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) < 11:
                continue
            try:
                test_name = parts[0]
                vertices = int(parts[1])
                edges = int(parts[2])
                exact_time = float(parts[3])
                approx_time = float(parts[4])
                exact_value = int(parts[5])
                approx_value = int(parts[6])
                quality = parts[7]
                difference = float(parts[8])
                percent_diff = float(parts[9])
                speedup_str = parts[10]
                speedup = float(speedup_str) if speedup_str != "N/A" else None
            except ValueError:
                continue

            data.append(
                {
                    "test_name": test_name,
                    "vertices": vertices,
                    "edges": edges,
                    "exact_time": exact_time,
                    "approx_time": approx_time,
                    "exact_value": exact_value,
                    "approx_value": approx_value,
                    "quality": quality,
                    "difference": difference,
                    "percent_diff": percent_diff,
                    "speedup": speedup,
                }
            )

    if not data:
        print(f"No usable rows found in {path}.")
        sys.exit(1)

    # Sort by number of vertices so plots look clean
    data.sort(key=lambda d: d["vertices"])
    return data


def plot_runtime(data, out_dir):
    """Plot runtime (wall clock) of exact vs approx as line graph with linear scale (decimal seconds)."""
    # Sort data by vertices for cleaner plot
    data_sorted = sorted(data, key=lambda d: (d["vertices"], d["edges"]))
    
    vertices = [d["vertices"] for d in data_sorted]
    exact_times = [d["exact_time"] for d in data_sorted]
    approx_times = [d["approx_time"] for d in data_sorted]
    
    # Create uniform test names for x-axis labels (same format as quality plot)
    size_groups = {}
    for d in data_sorted:
        v = d["vertices"]
        e = d["edges"]
        key = (v, e)
        if key not in size_groups:
            size_groups[key] = []
        size_groups[key].append(d)
    
    uniform_names = []
    for (v, e) in sorted(size_groups.keys()):
        group = size_groups[(v, e)]
        if len(group) == 1:
            uniform_names.append(f"{v}v_{e}")
        else:
            for idx, d in enumerate(group, 1):
                uniform_names.append(f"{v}v_{e}_{idx}")

    fig, ax = plt.subplots(1, 1, figsize=(max(16, len(data_sorted) * 0.65), 8))
    
    x_pos = range(len(data_sorted))
    
    # Plot as line graph
    line1 = ax.plot(x_pos, exact_times, "ro-", label="Exact (optimal)", linewidth=2.5, markersize=8, alpha=0.8)
    line2 = ax.plot(x_pos, approx_times, "gs-", label="Approximation", linewidth=2.5, markersize=8, alpha=0.8)
    
    # Add decimal values in parentheses next to each point
    for i, (x, exact_t, approx_t) in enumerate(zip(x_pos, exact_times, approx_times)):
        # Label for exact (above point)
        ax.text(x, exact_t, f'({exact_t:.3f})', 
                ha='center', va='bottom', fontsize=7, color='red', alpha=0.8)
        # Label for approx (above point)
        ax.text(x, approx_t, f'({approx_t:.3f})', 
                ha='center', va='bottom', fontsize=7, color='green', alpha=0.8)
    
    ax.set_xlabel("Test Case", fontsize=12, fontweight='bold')
    ax.set_ylabel("Runtime (seconds, log scale)", fontsize=12, fontweight='bold')
    ax.set_title("Exact vs Approximation Runtime (Wall Clock)\n(Log Scale with Decimal Values)", 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(uniform_names, rotation=45, ha='right', fontsize=8)
    ax.set_yscale("log")  # Log scale
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9)

    png_path = os.path.join(out_dir, "part_D_runtime_comparison.png")
    pdf_path = os.path.join(out_dir, "part_D_runtime_comparison.pdf")
    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    print(f"Saved runtime comparison plots to:\n  {png_path}\n  {pdf_path}")
    plt.close()


def plot_runtime_exact_only(data, out_dir):
    """Plot runtime (wall clock) of exact solution only as line graph with log scale."""
    # Sort data by vertices for cleaner plot
    data_sorted = sorted(data, key=lambda d: (d["vertices"], d["edges"]))
    
    vertices = [d["vertices"] for d in data_sorted]
    exact_times = [d["exact_time"] for d in data_sorted]
    
    # Create uniform test names for x-axis labels (same format as quality plot)
    size_groups = {}
    for d in data_sorted:
        v = d["vertices"]
        e = d["edges"]
        key = (v, e)
        if key not in size_groups:
            size_groups[key] = []
        size_groups[key].append(d)
    
    uniform_names = []
    for (v, e) in sorted(size_groups.keys()):
        group = size_groups[(v, e)]
        if len(group) == 1:
            uniform_names.append(f"{v}v_{e}")
        else:
            for idx, d in enumerate(group, 1):
                uniform_names.append(f"{v}v_{e}_{idx}")

    fig, ax = plt.subplots(1, 1, figsize=(max(16, len(data_sorted) * 0.65), 8))
    
    x_pos = range(len(data_sorted))
    
    # Plot as line graph - exact only
    ax.plot(x_pos, exact_times, "ro-", label="Exact (optimal)", linewidth=2.5, markersize=8, alpha=0.8)
    
    # Add decimal values in parentheses next to each point
    for i, (x, exact_t) in enumerate(zip(x_pos, exact_times)):
        # Label for exact (above point)
        ax.text(x, exact_t, f'({exact_t:.3f})', 
                ha='center', va='bottom', fontsize=7, color='red', alpha=0.8)
    
    ax.set_xlabel("Test Case", fontsize=12, fontweight='bold')
    ax.set_ylabel("Runtime (seconds, log scale)", fontsize=12, fontweight='bold')
    ax.set_title("Exact Solution Runtime (Wall Clock)\n(Log Scale with Decimal Values)", 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(uniform_names, rotation=45, ha='right', fontsize=8)
    ax.set_yscale("log")  # Log scale
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9)

    png_path = os.path.join(out_dir, "part_D_runtime_exact_only.png")
    pdf_path = os.path.join(out_dir, "part_D_runtime_exact_only.pdf")
    plt.tight_layout()
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    print(f"Saved exact-only runtime plot to:\n  {png_path}\n  {pdf_path}")
    plt.close()


def plot_quality(data, out_dir):
    """
    Plot solution quality as bar chart only (no line graph).
    Shows approximation performance as percentage of optimal.
    """
    # Sort data by vertices, then edges for better organization
    data_sorted = sorted(data, key=lambda d: (d["vertices"], d["edges"]))
    
    # Create uniform test names: group by (vertices, edges) and number duplicates
    # Format: Nv_M if unique, or Nv_M_1, Nv_M_2, etc. if duplicates exist
    size_groups = {}
    for d in data_sorted:
        v = d["vertices"]
        e = d["edges"]
        key = (v, e)
        if key not in size_groups:
            size_groups[key] = []
        size_groups[key].append(d)
    
    # Assign uniform names
    uniform_names = []
    for (v, e) in sorted(size_groups.keys()):
        group = size_groups[(v, e)]
        if len(group) == 1:
            # Only one test with this (v, e) combination - no suffix needed
            uniform_names.append(f"{v}v_{e}")
        else:
            # Multiple tests with same (v, e) - add suffix
            for idx, d in enumerate(group, 1):
                uniform_names.append(f"{v}v_{e}_{idx}")
    
    vertices = [d["vertices"] for d in data_sorted]
    exact_vals = [d["exact_value"] for d in data_sorted]
    approx_vals = [d["approx_value"] for d in data_sorted]
    qualities = [d["quality"] for d in data_sorted]
    test_names = uniform_names
    
    # Calculate error percentage for each test
    error_percentages = []
    for i in range(len(data_sorted)):
        if exact_vals[i] > 0:
            err_pct = (approx_vals[i] / exact_vals[i]) * 100.0
            error_percentages.append(err_pct)
        else:
            error_percentages.append(0.0)
    
    # Create single figure with moderate spacing
    fig, ax = plt.subplots(1, 1, figsize=(max(16, len(data_sorted) * 0.65), 8))
    
    # Color bars by quality
    bar_colors = ['#2ecc71' if q == 'OPTIMAL' else '#e67e22' for q in qualities]  # Green for optimal, orange for suboptimal
    
    # Create bars with moderate spacing (thinner bars, closer together than before but not as close as original)
    x_pos = range(len(data_sorted))
    bars = ax.bar(x_pos, error_percentages, color=bar_colors, alpha=0.8, 
                  edgecolor='black', linewidth=1.5, width=0.6)
    
    # Add 100% reference line
    ax.axhline(y=100, color='red', linestyle='--', linewidth=2.5, 
               label='100% (Perfect)', alpha=0.8, zorder=0)
    
    # Add value labels on bars - percentage above, values below
    for i, (bar, err_pct, exact_val, approx_val) in enumerate(zip(bars, error_percentages, exact_vals, approx_vals)):
        height = bar.get_height()
        x_center = bar.get_x() + bar.get_width()/2.
        
        # Percentage label above bar
        label_y = height + 0.3 if height < 99.5 else height + 0.15
        ax.text(x_center, label_y,
                f'{err_pct:.1f}%',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Value labels below bar (exact/approx) - only if there's space
        # Position at bottom of bar or slightly below
        value_y = max(85, height - 1.5)  # Don't go below y-axis minimum
        if height > 87:  # Only show if bar is tall enough
            ax.text(x_center, value_y,
                    f'{exact_val}/{approx_val}',
                    ha='center', va='top', fontsize=7,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='gray', linewidth=0.5))
    
    # Create x-axis labels with uniform format
    x_labels = []
    for name in test_names:
        # Use uniform format: Nv_M or Nv_M_K
        x_labels.append(name)
    
    ax.set_xlabel("Test Case (vertices shown)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Approximation Quality (% of optimal)", fontsize=12, fontweight='bold')
    ax.set_title("Approximation Solution Quality vs Optimal\n(Percentage = Approx/Exact × 100%)", 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
    ax.set_ylim([85, 102.5])  # Extended range to show labels clearly
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    
    # Add statistics text box - moved further into top left corner
    optimal_count = sum(1 for q in qualities if q == "OPTIMAL")
    avg_error = sum(error_percentages) / len(error_percentages) if error_percentages else 0
    min_error = min(error_percentages)
    max_error = max(error_percentages)
    stats_text = f"Statistics:\n"
    stats_text += f"Total Tests: {len(data_sorted)}\n"
    stats_text += f"Optimal: {optimal_count} ({optimal_count/len(data_sorted)*100:.1f}%)\n"
    stats_text += f"Avg Quality: {avg_error:.2f}%\n"
    stats_text += f"Range: {min_error:.2f}% - {max_error:.2f}%"
    ax.text(0.01, 0.99, stats_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', horizontalalignment='left',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            family='monospace')
    
    plt.tight_layout()
    
    png_path = os.path.join(out_dir, "part_D_solution_quality.png")
    pdf_path = os.path.join(out_dir, "part_D_solution_quality.pdf")
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.savefig(pdf_path, bbox_inches='tight')
    print(f"Saved solution-quality plot (bar chart only) to:\n  {png_path}\n  {pdf_path}")
    plt.close()


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # project root is the parent of part_D
    project_root = os.path.dirname(script_dir)

    # Prefer the Part D averaged data if it exists; otherwise fall back
    part_d_data = os.path.join(script_dir, "comparison_data_part_D.txt")
    if os.path.exists(part_d_data):
        data_path = part_d_data
    else:
        data_path = os.path.join(project_root, "comparison_data.txt")

    data = read_comparison_data(data_path)

    print(f"Loaded {len(data)} comparison rows from {data_path}")
    print("Generating Part D plots...")

    plot_runtime(data, script_dir)
    plot_runtime_exact_only(data, script_dir)
    plot_quality(data, script_dir)

    print("Done.")


if __name__ == "__main__":
    main()


