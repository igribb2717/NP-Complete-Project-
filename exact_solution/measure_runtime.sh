#!/bin/bash

# CS 412 Longest Path - Runtime Measurement Script
# This script measures wall clock time for all test cases and generates data for plotting

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEST_DIR="$SCRIPT_DIR/test_cases"
OUTPUT_FILE="$SCRIPT_DIR/runtime_data.txt"

echo "Measuring runtime for all test cases..."
echo "This may take a while, especially for large test cases..."
echo ""

# Clear output file
echo "# Test Case | Vertices | Edges | Runtime (seconds)" > "$OUTPUT_FILE"
echo "# Format: test_name vertices edges runtime_seconds" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Function to count vertices and edges in a test file
count_graph_size() {
    local file=$1
    local first_line=$(head -1 "$file")
    echo "$first_line"
}

# Test cases in order of increasing size
test_cases=(
    "test_input_small_1"
    "test_input_small_2"
    "test_input_1"
    "test_input_2"
    "test_input_3"
    "test_input_4"
    "test_input_5"
    "test_input_medium_1"
    "test_input_6"
    "test_input_7"
    "test_input_medium_2"
    "test_input_8"
    "test_input_large_1"
    "test_input_large_2"
    "test_input_very_large"
    "test_input_large"
    "test_input_extreme"
)

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
    
    echo "Running $test_case (n=$vertices, m=$edges)..."
    echo -n "  "
    
    # Measure runtime using time command
    # Format: real time in seconds
    runtime=$( (time -p python3 "$SCRIPT_DIR/cs412_longestpath_exact.py" < "$test_file" > /dev/null 2>&1) 2>&1 | grep real | awk '{print $2}')
    
    if [ -z "$runtime" ]; then
        runtime="ERROR"
        echo "  ERROR: Could not measure runtime"
    else
        echo "  Runtime: ${runtime}s"
    fi
    
    # Write to output file
    echo "$test_case $vertices $edges $runtime" >> "$OUTPUT_FILE"
    echo ""
done

echo "Runtime data saved to: $OUTPUT_FILE"
echo ""
echo "To visualize the data, run:"
echo "  python3 plot_runtime.py"

