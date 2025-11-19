#!/bin/bash

# CS 412 Longest Path - Timing Test Suite
# This script runs timing tests and reports duration in minutes and seconds

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEST_DIR="$SCRIPT_DIR/test_cases"
APPROX_SCRIPT="$SCRIPT_DIR/../approx_solution/cs412_longestpath_approx.py"
EXACT_SCRIPT="$SCRIPT_DIR/../exact_solution/cs412_longestpath_exact.py"

# Default to approximation, but allow override via command line argument
SOLUTION_TYPE="approx"
if [ "$1" = "--exact" ] || [ "$1" = "-e" ]; then
    SOLUTION_TYPE="exact"
elif [ "$1" = "--approx" ] || [ "$1" = "-a" ]; then
    SOLUTION_TYPE="approx"
elif [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: $0 [--exact|--approx]"
    echo "  --exact, -e    Use the exact solution (slower, optimal)"
    echo "  --approx, -a   Use the approximation solution (faster, default)"
    exit 0
fi

# Set the script to use
if [ "$SOLUTION_TYPE" = "exact" ]; then
    SOLVER_SCRIPT="$EXACT_SCRIPT"
    SOLVER_NAME="Exact"
else
    SOLVER_SCRIPT="$APPROX_SCRIPT"
    SOLVER_NAME="Approximation"
fi

echo "=========================================="
echo "CS 412 Longest Path - Timing Test Suite"
echo "Using: ${SOLVER_NAME} Solution"
echo "=========================================="
echo ""

# Check if Python script exists
if [ ! -f "$SOLVER_SCRIPT" ]; then
    echo -e "${RED}Error: Solver script not found at $SOLVER_SCRIPT${NC}"
    exit 1
fi

# Check if test cases directory exists
if [ ! -d "$TEST_DIR" ]; then
    echo -e "${YELLOW}Test cases directory not found. Generating test cases...${NC}"
    python3 "$SCRIPT_DIR/generate_timing_tests.py"
    echo ""
fi

# Check if test cases exist
if [ ! -f "$TEST_DIR/test_01.txt" ]; then
    echo -e "${RED}Error: Test cases not found in $TEST_DIR${NC}"
    echo "Please run: python3 $SCRIPT_DIR/generate_timing_tests.py"
    exit 1
fi

# Function to get graph stats (vertices and edges)
get_graph_stats() {
    local test_file=$1
    local first_line=$(head -n 1 "$test_file")
    echo "$first_line"
}

# Function to format time in minutes and seconds
format_time() {
    local total_seconds=$1
    local minutes=$((total_seconds / 60))
    local seconds=$((total_seconds % 60))
    
    if [ $minutes -eq 0 ]; then
        printf "%d seconds" $seconds
    else
        printf "%d minute(s) %d second(s)" $minutes $seconds
    fi
}

# Function to run a single test
run_test() {
    local test_num=$1
    local test_num_formatted=$(printf "%02d" $test_num)
    local test_file="$TEST_DIR/test_${test_num_formatted}.txt"
    
    if [ ! -f "$test_file" ]; then
        echo -e "${RED}Test file not found: $test_file${NC}"
        return 1
    fi
    
    # Get graph stats
    local stats=$(get_graph_stats "$test_file")
    local vertices=$(echo $stats | cut -d' ' -f1)
    local edges=$(echo $stats | cut -d' ' -f2)
    
    echo -e "${CYAN}Test ${test_num}:${NC} ${vertices} vertices, ${edges} edges"
    echo -n "Running... "
    
    # Run the test and measure time
    start_time=$(date +%s)
    python3 "$SOLVER_SCRIPT" < "$test_file" > /dev/null 2>&1
    exit_code=$?
    end_time=$(date +%s)
    
    elapsed=$((end_time - start_time))
    
    if [ $exit_code -eq 0 ]; then
        formatted_time=$(format_time $elapsed)
        echo -e "${GREEN}Completed${NC}"
        echo -e "  Duration: ${YELLOW}${formatted_time}${NC}"
        echo -e "  Vertices: ${vertices}, Edges: ${edges}"
    else
        echo -e "${RED}Failed${NC} (exit code: $exit_code)"
    fi
    
    echo ""
}

# Run all tests
echo -e "${BLUE}Running timing tests...${NC}"
echo ""

total_start=$(date +%s)

for i in {1..10}; do
    run_test $i
done

total_end=$(date +%s)
total_elapsed=$((total_end - total_start))
total_formatted=$(format_time $total_elapsed)

echo "=========================================="
echo -e "${GREEN}All tests completed!${NC}"
echo -e "Total time: ${YELLOW}${total_formatted}${NC}"
echo "=========================================="

