#!/usr/bin/env python3
"""Find worst performing cases for improved approximation."""

import json

with open('improved_approx_full_results.json', 'r') as f:
    data = json.load(f)

# Sort by worst performance (lowest ratio, then largest difference)
worst = sorted(data, key=lambda x: (x['ratio'], -x['difference']))[:20]

print("20 Worst Performing Cases for Improved Approximation:")
print("=" * 80)
for i, w in enumerate(worst, 1):
    print(f"{i:2d}. {w['test_file']}: {w['percentage']:.2f}% "
          f"(Improved={w['improved_length']}, Exact={w['exact_length']}, Diff={w['difference']})")

# Also create CSV for worst 10
import csv
with open('worst_improved_cases.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Test File', 'Improved Length', 'Exact Length', 'Percentage', 'Difference'])
    for w in worst[:10]:
        writer.writerow([w['test_file'], w['improved_length'], w['exact_length'], 
                        f"{w['percentage']:.2f}%", w['difference']])

print(f"\nCreated worst_improved_cases.csv with top 10 worst cases")

