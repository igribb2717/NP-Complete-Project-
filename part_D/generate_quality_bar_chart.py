#!/usr/bin/env python3
"""
Generate bar chart showing Greedy solution quality (% of optimal).
Green bars for 100% (optimal), orange to red for suboptimal.
"""

import os
import sys
import csv

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Error: matplotlib is not installed.")
    print("Install with: pip install matplotlib numpy")
    sys.exit(1)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CSV_FILE = os.path.join(PROJECT_ROOT, "part_D", "exact_vs_greedy_comparison.csv")
PNG_FILE = os.path.join(PROJECT_ROOT, "part_D", "greedy_quality_bar_chart.png")
PDF_FILE = os.path.join(PROJECT_ROOT, "part_D", "greedy_quality_bar_chart.pdf")


def read_data():
    """Read comparison data from CSV."""
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found.")
        print("Please run generate_exact_vs_greedy.py first.")
        sys.exit(1)

    data = []
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                "test_name": row["test_name"],
                "vertices": int(row["vertices"]),
                "edges": int(row["edges"]),
                "exact_value": int(row["exact_value"]),
                "greedy_value": int(row["greedy_value"]),
                "quality_percent": float(row["quality_percent"]),
            })

    if not data:
        print("No data found in CSV file.")
        sys.exit(1)

    # Sort by complexity: edges first, then vertices
    data.sort(key=lambda d: (d["edges"], d["vertices"]))
    return data


def plot_quality_bar_chart(data):
    """Create bar chart showing quality percentage."""
    # Create uniform test names
    size_counts = {}
    uniform_names = []
    for d in data:
        v = d["vertices"]
        e = d["edges"]
        key = (v, e)
        if key not in size_counts:
            size_counts[key] = 0
        size_counts[key] += 1
        count = size_counts[key]

        if count == 1:
            uniform_names.append(f"{v}v_{e}")
        else:
            uniform_names.append(f"{v}v_{e}_{count}")

    quality_percentages = [d["quality_percent"] for d in data]
    exact_values = [d["exact_value"] for d in data]
    greedy_values = [d["greedy_value"] for d in data]

    # Color bars: green for 100%, orange to red gradient for suboptimal
    bar_colors = []
    for pct in quality_percentages:
        if pct >= 99.9:  # Optimal (100%)
            bar_colors.append('#2ecc71')  # Green
        elif pct >= 95:  # Good (95-99.9%)
            bar_colors.append('#f39c12')  # Orange
        elif pct >= 90:  # Fair (90-95%)
            bar_colors.append('#e67e22')  # Dark orange
        else:  # Poor (<90%)
            bar_colors.append('#e74c3c')  # Red

    fig, ax = plt.subplots(1, 1, figsize=(max(16, len(data) * 0.65), 8))

    x_pos = range(len(data))
    bars = ax.bar(x_pos, quality_percentages, color=bar_colors, alpha=0.8, 
                  edgecolor='black', linewidth=1.5, width=0.6)

    # Add 100% reference line
    ax.axhline(y=100, color='red', linestyle='--', linewidth=2.5, 
               label='100% (Optimal)', alpha=0.8, zorder=0)

    # Add percentage labels on bars
    for i, (bar, pct, exact_val, greedy_val) in enumerate(
        zip(bars, quality_percentages, exact_values, greedy_values)
    ):
        height = bar.get_height()
        x_center = bar.get_x() + bar.get_width()/2.

        # Percentage label above bar
        label_y = height + 0.5 if height < 99.5 else height + 0.2
        ax.text(x_center, label_y, f'{pct:.1f}%', ha='center', va='bottom', 
                fontsize=9, fontweight='bold')

        # Value labels inside bar if there's space
        if height > 87:
            ax.text(x_center, max(87, height - 1.5), f'{exact_val}/{greedy_val}', 
                    ha='center', va='top', fontsize=7,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                    alpha=0.7, edgecolor='gray', linewidth=0.5))

    ax.set_xlabel("Test Case", fontsize=12, fontweight="bold")
    ax.set_ylabel("Solution Quality (% of optimal)", fontsize=12, fontweight="bold")
    ax.set_title("Greedy Solution Quality vs Optimal\n(Percentage = Greedy/Exact × 100%)", 
                 fontsize=14, fontweight="bold", pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(uniform_names, rotation=45, ha="right", fontsize=8)
    ax.set_ylim([80, 102.5])  # Extended range to show all bars clearly
    ax.grid(True, alpha=0.3, axis="y", linestyle="--")
    ax.legend(loc="upper right", fontsize=11, framealpha=0.9)

    # Add statistics text box
    optimal_count = sum(1 for pct in quality_percentages if pct >= 99.9)
    avg_quality = sum(quality_percentages) / len(quality_percentages)
    min_quality = min(quality_percentages)
    max_quality = max(quality_percentages)
    
    stats_text = f"Statistics:\n"
    stats_text += f"Total Tests: {len(data)}\n"
    stats_text += f"Optimal (100%): {optimal_count} ({optimal_count/len(data)*100:.1f}%)\n"
    stats_text += f"Avg Quality: {avg_quality:.2f}%\n"
    stats_text += f"Range: {min_quality:.2f}% - {max_quality:.2f}%"
    
    ax.text(0.01, 0.99, stats_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', horizontalalignment='left',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            family='monospace')

    plt.tight_layout()
    plt.savefig(PNG_FILE, dpi=300, bbox_inches="tight")
    plt.savefig(PDF_FILE, bbox_inches="tight")
    print(f"Bar chart saved to:\n  {PNG_FILE}\n  {PDF_FILE}")
    plt.close()


def main():
    print("=" * 80)
    print("Greedy Solution Quality Bar Chart")
    print("=" * 80)
    print()

    print("Reading data from CSV...")
    data = read_data()

    print(f"Loaded {len(data)} test cases")
    print("Generating bar chart...")
    plot_quality_bar_chart(data)

    print()
    print("=" * 80)
    print("Complete!")
    print(f"Graph files: {PNG_FILE}, {PDF_FILE}")
    print("=" * 80)


if __name__ == "__main__":
    main()

