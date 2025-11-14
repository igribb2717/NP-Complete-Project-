#!/bin/bash

# CS 412 Longest Path - Solution Comparison Script
# This script compares the exact and approximation solutions on the same test cases
# It measures runtime and solution quality for both approaches

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get directories
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EXACT_DIR="$SCRIPT_DIR/exact_solution"
APPROX_DIR="$SCRIPT_DIR/approx_solution"
OUTPUT_FILE="$SCRIPT_DIR/comparison_results.txt"

echo "=========================================="
echo "CS 412 Longest Path - Solution Comparison"
echo "=========================================="
echo ""

# Check if scripts exist
if [ ! -f "$EXACT_DIR/cs412_longestpath_exact.py" ]; then
    echo -e "${RED}Error: Exact solution not found!${NC}"
    exit 1
fi

if [ ! -f "$APPROX_DIR/cs412_longestpath_approx.py" ]; then
    echo -e "${RED}Error: Approximation solution not found!${NC}"
    exit 1
fi

# Function to measure runtime and get solution
measure_solution() {
    local script=$1
    local input_file=$2
    
    # Measure runtime and capture output
    local start_time=$(date +%s.%N)
    local output=$(python3 "$script" < "$input_file" 2>&1)
    local end_time=$(date +%s.%N)
    
    # Calculate runtime
    local runtime=$(echo "$end_time - $start_time" | bc)
    
    # Extract path length (first line)
    local path_length=$(echo "$output" | head -1)
    
    echo "$runtime|$path_length|$output"
}

# Function to compare solutions on a test case
compare_test() {
    local test_file=$1
    local test_name=$(basename "$test_file")
    local description=$2
    
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}Test: $test_name${NC}"
    echo -e "${CYAN}$description${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
    
    # Get graph size
    local first_line=$(head -1 "$test_file")
    local vertices=$(echo $first_line | awk '{print $1}')
    local edges=$(echo $first_line | awk '{print $2}')
    echo "Graph: $vertices vertices, $edges edges"
    echo ""
    
    # Run exact solution
    echo -e "${BLUE}Running EXACT solution...${NC}"
    local exact_result=$(measure_solution "$EXACT_DIR/cs412_longestpath_exact.py" "$test_file")
    local exact_runtime=$(echo "$exact_result" | cut -d'|' -f1)
    local exact_value=$(echo "$exact_result" | cut -d'|' -f2)
    local exact_output=$(echo "$exact_result" | cut -d'|' -f3-)
    
    echo "  Runtime: ${exact_runtime}s"
    echo "  Path length: $exact_value"
    echo "  Path: $(echo "$exact_output" | tail -1)"
    echo ""
    
    # Run approximation solution
    echo -e "${GREEN}Running APPROXIMATION solution...${NC}"
    local approx_result=$(measure_solution "$APPROX_DIR/cs412_longestpath_approx.py" "$test_file")
    local approx_runtime=$(echo "$approx_result" | cut -d'|' -f1)
    local approx_value=$(echo "$approx_result" | cut -d'|' -f2)
    local approx_output=$(echo "$approx_result" | cut -d'|' -f3-)
    
    echo "  Runtime: ${approx_runtime}s"
    echo "  Path length: $approx_value"
    echo "  Path: $(echo "$approx_output" | tail -1)"
    echo ""
    
    # Compare results
    echo -e "${YELLOW}Comparison:${NC}"
    
    # Runtime comparison
    local speedup=$(echo "scale=2; $exact_runtime / $approx_runtime" | bc 2>/dev/null || echo "N/A")
    if [ "$speedup" != "N/A" ] && [ $(echo "$exact_runtime > 0" | bc) -eq 1 ]; then
        echo "  Speedup: ${speedup}x faster (approximation vs exact)"
    else
        echo "  Speedup: Approximation is much faster (exact took too long or approximation was instant)"
    fi
    
    # Solution quality comparison
    if [ "$exact_value" -eq "$approx_value" ]; then
        echo -e "  Solution Quality: ${GREEN}OPTIMAL${NC} (approximation found optimal solution)"
        local quality="OPTIMAL"
        local difference=0
        local percent_diff=0
    else
        local difference=$(echo "$exact_value - $approx_value" | bc)
        local percent_diff=$(echo "scale=2; ($difference * 100) / $exact_value" | bc)
        echo -e "  Solution Quality: ${YELLOW}SUBOPTIMAL${NC}"
        echo "  Difference: $difference (approximation is $difference units shorter)"
        echo "  Percentage: ${percent_diff}% below optimal"
        local quality="SUBOPTIMAL"
    fi
    
    echo ""
    
    # Save to results file
    echo "$test_name|$vertices|$edges|$exact_runtime|$approx_runtime|$exact_value|$approx_value|$quality|$difference|$percent_diff" >> "$OUTPUT_FILE"
}

# Clear results file
echo "# Test Case | Vertices | Edges | Exact Runtime | Approx Runtime | Exact Value | Approx Value | Quality | Difference | Percent Diff" > "$OUTPUT_FILE"
echo "# Format: test_name|vertices|edges|exact_time|approx_time|exact_length|approx_length|quality|diff|percent" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Test cases to compare (use smaller ones that exact can handle)
echo "Selecting test cases that exact solution can handle..."
echo ""

# Small test cases
if [ -f "$APPROX_DIR/test_cases/test_small_1" ]; then
    compare_test "$APPROX_DIR/test_cases/test_small_1" "Small graph (3 vertices)"
fi

if [ -f "$APPROX_DIR/test_cases/test_small_2" ]; then
    compare_test "$APPROX_DIR/test_cases/test_small_2" "Small graph (4 vertices)"
fi

if [ -f "$APPROX_DIR/test_cases/test_medium_1" ]; then
    compare_test "$APPROX_DIR/test_cases/test_medium_1" "Medium graph (5 vertices)"
fi

if [ -f "$APPROX_DIR/test_cases/test_medium_2" ]; then
    compare_test "$APPROX_DIR/test_cases/test_medium_2" "Medium graph (6 vertices)"
fi

if [ -f "$APPROX_DIR/test_cases/test_large_1" ]; then
    compare_test "$APPROX_DIR/test_cases/test_large_1" "Large graph (10 vertices)"
fi

if [ -f "$APPROX_DIR/test_cases/test_nonoptimal" ]; then
    compare_test "$APPROX_DIR/test_cases/test_nonoptimal" "Non-optimal test case"
fi

# Summary
echo ""
echo "=========================================="
echo "Summary"
echo "=========================================="
echo ""
echo "Results saved to: $OUTPUT_FILE"
echo ""
echo "To view results in a table:"
echo "  cat $OUTPUT_FILE"
echo ""

