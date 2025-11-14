#!/bin/bash

# CS 412 Longest Path - Detailed Solution Comparison
# This script creates a detailed comparison report with plots-ready data

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EXACT_DIR="$SCRIPT_DIR/exact_solution"
APPROX_DIR="$SCRIPT_DIR/approx_solution"
OUTPUT_FILE="$SCRIPT_DIR/comparison_data.txt"
SUMMARY_FILE="$SCRIPT_DIR/comparison_summary.txt"

echo "=========================================="
echo "CS 412 Longest Path - Detailed Comparison"
echo "Generating data for plots and analysis"
echo "=========================================="
echo ""

# Check dependencies
command -v bc >/dev/null 2>&1 || { echo "Error: bc is required but not installed."; exit 1; }

# Initialize output files
echo "# Test Case | Vertices | Edges | Exact Runtime (s) | Approx Runtime (s) | Exact Value | Approx Value | Quality | Difference | Percent Diff | Speedup" > "$OUTPUT_FILE"
echo "# Format for plotting: test_name vertices edges exact_time approx_time exact_length approx_length quality diff percent speedup" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "Comparison Summary" > "$SUMMARY_FILE"
echo "==================" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

# Function to measure with better precision
measure_solution_precise() {
    local script=$1
    local input_file=$2
    
    # Use Python's time for better precision
    local result=$(python3 -c "
import sys
import time
import subprocess
import re

start = time.time()
proc = subprocess.run(['python3', '$script'], stdin=open('$input_file'), 
                      capture_output=True, text=True)
elapsed = time.time() - start
output = proc.stdout.strip()
# Get first line (path length) - extract first number
lines = output.split('\n')
if lines:
    first_line = lines[0].strip()
    # Extract first integer from the line
    match = re.search(r'^\d+', first_line)
    path_length = int(match.group()) if match else 0
else:
    path_length = 0
print(f'{elapsed}|{path_length}|{output}')
" 2>/dev/null)
    
    echo "$result"
}

# Test cases (smaller ones that exact can handle quickly)
test_cases=(
    "$APPROX_DIR/test_cases/test_small_1:Small:3:3"
    "$APPROX_DIR/test_cases/test_small_2:Small:4:6"
    "$APPROX_DIR/test_cases/test_medium_1:Medium:5:10"
    "$APPROX_DIR/test_cases/test_medium_2:Medium:6:9"
    "$APPROX_DIR/test_cases/test_large_1:Large:10:20"
    "$APPROX_DIR/test_cases/test_nonoptimal:NonOptimal:6:8"
)

total_tests=0
optimal_count=0
suboptimal_count=0
total_speedup=0
speedup_count=0

for test_info in "${test_cases[@]}"; do
    IFS=':' read -r test_file category vertices edges <<< "$test_info"
    
    if [ ! -f "$test_file" ]; then
        continue
    fi
    
    test_name=$(basename "$test_file")
    echo -e "${CYAN}Processing: $test_name${NC}"
    
    # Run exact
    echo "  Running exact solution..."
    exact_result=$(measure_solution_precise "$EXACT_DIR/cs412_longestpath_exact.py" "$test_file")
    exact_runtime=$(echo "$exact_result" | head -1 | cut -d'|' -f1)
    exact_value=$(echo "$exact_result" | head -1 | cut -d'|' -f2)
    
    # Run approximation
    echo "  Running approximation solution..."
    approx_result=$(measure_solution_precise "$APPROX_DIR/cs412_longestpath_approx.py" "$test_file")
    approx_runtime=$(echo "$approx_result" | head -1 | cut -d'|' -f1)
    approx_value=$(echo "$approx_result" | head -1 | cut -d'|' -f2)
    
    # Calculate metrics
    if [ "$exact_value" -eq "$approx_value" ]; then
        quality="OPTIMAL"
        difference=0
        percent_diff=0
        ((optimal_count++))
    else
        quality="SUBOPTIMAL"
        difference=$(echo "$exact_value - $approx_value" | bc)
        percent_diff=$(echo "scale=2; ($difference * 100) / $exact_value" | bc)
        ((suboptimal_count++))
    fi
    
    # Calculate speedup
    if [ $(echo "$approx_runtime > 0" | bc 2>/dev/null || echo "0") -eq 1 ] && [ $(echo "$exact_runtime > 0" | bc 2>/dev/null || echo "0") -eq 1 ]; then
        speedup=$(echo "scale=2; $exact_runtime / $approx_runtime" | bc 2>/dev/null || echo "N/A")
        if [ "$speedup" != "N/A" ]; then
            total_speedup=$(echo "$total_speedup + $speedup" | bc 2>/dev/null || echo "$total_speedup")
            ((speedup_count++))
        fi
    else
        speedup="N/A"
    fi
    
    # Write to output file
    echo "$test_name|$vertices|$edges|$exact_runtime|$approx_runtime|$exact_value|$approx_value|$quality|$difference|$percent_diff|$speedup" >> "$OUTPUT_FILE"
    
    ((total_tests++))
    echo "  ✓ Complete"
    echo ""
done

# Generate summary
echo "Test Results Summary" >> "$SUMMARY_FILE"
echo "-------------------" >> "$SUMMARY_FILE"
echo "Total tests: $total_tests" >> "$SUMMARY_FILE"
echo "Optimal solutions: $optimal_count" >> "$SUMMARY_FILE"
echo "Suboptimal solutions: $suboptimal_count" >> "$SUMMARY_FILE"
if [ $speedup_count -gt 0 ]; then
    avg_speedup=$(echo "scale=2; $total_speedup / $speedup_count" | bc)
    echo "Average speedup: ${avg_speedup}x" >> "$SUMMARY_FILE"
fi
echo "" >> "$SUMMARY_FILE"
echo "Data saved to: $OUTPUT_FILE" >> "$SUMMARY_FILE"

echo "=========================================="
echo "Comparison Complete!"
echo "=========================================="
echo ""
echo "Results saved to:"
echo "  - $OUTPUT_FILE (detailed data for plotting)"
echo "  - $SUMMARY_FILE (summary statistics)"
echo ""
echo "View results:"
echo "  cat $OUTPUT_FILE"
echo "  cat $SUMMARY_FILE"
echo ""

