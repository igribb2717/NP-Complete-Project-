#!/bin/bash

# CS 412 Longest Path - Approximation Wall Clock Runtime Measurement
# This script measures wall clock time for approximation test cases used in plots
# For Part D: Approximation Presentation

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APPROX_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
APPROX_SCRIPT="$APPROX_DIR/cs412_longestpath_approx.py"

echo "=========================================="
echo "Approximation Solution Wall Clock Runtime"
echo "Measuring runtime for test cases used in plots"
echo "=========================================="
echo ""

# Test cases used for Part D plots (from additional_test_cases)
# These are the test cases that were used to generate the comparison plots
test_cases=(
    "test_8v_1.txt"
    "test_8v_2.txt"
    "test_8v_3.txt"
    "test_8v_4.txt"
    "test_8v_5.txt"
    "test_9v_1.txt"
    "test_9v_2.txt"
    "test_9v_3.txt"
    "test_9v_4.txt"
    "test_9v_5.txt"
    "test_10v_1.txt"
    "test_10v_2.txt"
    "test_10v_3.txt"
    "test_10v_4.txt"
    "test_10v_5.txt"
    "test_11v_1.txt"
    "test_11v_2.txt"
    "test_11v_3.txt"
    "test_11v_4.txt"
    "test_11v_5.txt"
)

# Check if we're in the right directory or need to use part_D test cases
PART_D_TEST_DIR="$SCRIPT_DIR/../../part_D/additional_test_cases"

if [ -d "$PART_D_TEST_DIR" ]; then
    TEST_DIR="$PART_D_TEST_DIR"
    echo "Using Part D additional test cases from: $TEST_DIR"
else
    # Fallback to local test cases
    TEST_DIR="$SCRIPT_DIR"
    echo "Using local test cases from: $TEST_DIR"
fi

echo ""

# Function to count vertices and edges
count_graph_size() {
    local file=$1
    if [ -f "$file" ]; then
        local first_line=$(head -1 "$file")
        echo "$first_line"
    else
        echo "0 0"
    fi
}

# Output header
echo "Test Case | Vertices | Edges | Runtime (seconds)"
echo "------------------------------------------------"

total_runtime=0
count=0

for test_case in "${test_cases[@]}"; do
    test_file="$TEST_DIR/$test_case"
    
    if [ ! -f "$test_file" ]; then
        echo "Warning: $test_file not found, skipping..."
        continue
    fi
    
    # Get graph size
    size_info=$(count_graph_size "$test_file")
    vertices=$(echo $size_info | awk '{print $1}')
    edges=$(echo $size_info | awk '{print $2}')
    
    echo -n "Running $test_case (n=$vertices, m=$edges)... "
    
    # Measure runtime using time command
    # Format: real time in seconds
    runtime=$( (time -p python3 "$APPROX_SCRIPT" < "$test_file" > /dev/null 2>&1) 2>&1 | grep real | awk '{print $2}')
    
    if [ -z "$runtime" ] || [ "$runtime" = "ERROR" ]; then
        echo "ERROR"
    else
        echo "${runtime}s"
        total_runtime=$(echo "$total_runtime + $runtime" | bc 2>/dev/null || echo "$total_runtime")
        count=$((count + 1))
    fi
done

echo ""
echo "=========================================="
echo "Summary:"
echo "  Test cases run: $count"
if [ $count -gt 0 ] && command -v bc >/dev/null 2>&1; then
    avg_runtime=$(echo "scale=4; $total_runtime / $count" | bc)
    echo "  Total runtime: ${total_runtime}s"
    echo "  Average runtime: ${avg_runtime}s"
fi
echo "=========================================="

