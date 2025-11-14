#!/bin/bash

# CS 412 Longest Path - Exact Solution Test Runner
# This script runs the exact solution on all test cases and illustrates
# how runtime (wall clock) varies with different input sizes.

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEST_DIR="$SCRIPT_DIR/test_cases"

echo "=========================================="
echo "CS 412 Longest Path - Exact Solution Tests"
echo "Runtime Analysis: Demonstrating exponential growth"
echo "=========================================="
echo ""

# Check if Python script exists
if [ ! -f "$SCRIPT_DIR/cs412_longestpath_exact.py" ]; then
    echo -e "${RED}Error: cs412_longestpath_exact.py not found!${NC}"
    exit 1
fi

# Function to run test and show timing
run_test() {
    local test_name=$1
    local vertices=$2
    local edges=$3
    local description=$4
    local is_slow=$5
    
    echo -e "${GREEN}${description}${NC}"
    echo "  Test file: $test_name"
    echo "  Graph size: $vertices vertices, $edges edges"
    if [ "$is_slow" = "true" ]; then
        echo -e "  ${YELLOW}WARNING: This test case may take a VERY LONG TIME (>20 minutes)${NC}"
        echo "  Starting at $(date)"
    fi
    echo ""
    
    time python3 "$SCRIPT_DIR/cs412_longestpath_exact.py" < "$TEST_DIR/$test_name"
    
    if [ "$is_slow" = "true" ]; then
        echo "  Completed at $(date)"
    fi
    echo ""
    echo "---"
    echo ""
}

# Test cases organized by size to show runtime progression

# Very Small (2-3 vertices) - Should run in < 1 second
echo -e "${BLUE}=== VERY SMALL TEST CASES (< 1 second) ===${NC}"
run_test "test_input_small_1" "2" "1" "Test 1: Very small graph (2 vertices, 1 edge)" "false"
run_test "test_input_small_2" "3" "2" "Test 2: Very small graph (3 vertices, 2 edges)" "false"
run_test "test_input_1" "3" "3" "Test 3: Small graph (3 vertices, 3 edges)" "false"

# Small (4-5 vertices) - Should run in < 5 seconds
echo -e "${BLUE}=== SMALL TEST CASES (< 5 seconds) ===${NC}"
run_test "test_input_2" "4" "6" "Test 4: Small graph (4 vertices, 6 edges)" "false"
run_test "test_input_3" "5" "10" "Test 5: Small graph (5 vertices, 10 edges)" "false"

# Medium (6-9 vertices) - Should run in seconds to minutes
echo -e "${BLUE}=== MEDIUM TEST CASES (seconds to minutes) ===${NC}"
run_test "test_input_4" "6" "9" "Test 6: Medium graph (6 vertices, 9 edges)" "false"
run_test "test_input_5" "8" "12" "Test 7: Medium graph (8 vertices, 12 edges)" "false"
run_test "test_input_medium_1" "7" "12" "Test 8: Medium graph (7 vertices, 12 edges)" "false"
run_test "test_input_6" "10" "20" "Test 9: Medium-large graph (10 vertices, 20 edges)" "false"
run_test "test_input_medium_2" "9" "15" "Test 10: Medium graph (9 vertices, 15 edges)" "false"

# Large (10-15 vertices) - Should run in minutes
echo -e "${BLUE}=== LARGE TEST CASES (minutes) ===${NC}"
run_test "test_input_7" "12" "18" "Test 11: Large graph (12 vertices, 18 edges)" "false"
run_test "test_input_8" "15" "30" "Test 12: Large graph (15 vertices, 30 edges)" "false"
run_test "test_input_large_1" "11" "20" "Test 13: Large graph (11 vertices, 20 edges)" "false"
run_test "test_input_large_2" "13" "25" "Test 14: Large graph (13 vertices, 25 edges)" "false"

# Very Large (18+ vertices) - Should run for > 20 minutes
echo -e "${YELLOW}=== VERY LARGE TEST CASES (> 20 MINUTES) ===${NC}"
run_test "test_input_very_large" "20" "40" "Test 15: Very large graph (20 vertices, 40 edges)" "true"
run_test "test_input_large" "18" "35" "Test 16: Very large graph (18 vertices, 35 edges) - EXPECTED >20 MINUTES" "true"

# Extreme (22+ vertices) - Will take hours
echo -e "${RED}=== EXTREME TEST CASES (HOURS - OPTIONAL) ===${NC}"
echo -e "${RED}WARNING: The following test case will take HOURS to complete.${NC}"
echo -e "${RED}You may want to skip this or run it separately.${NC}"
echo ""
read -p "Run extreme test case? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    run_test "test_input_extreme" "22" "45" "Test 17: Extreme graph (22 vertices, 45 edges) - EXPECTED HOURS" "true"
else
    echo -e "${YELLOW}Skipping extreme test case.${NC}"
    echo ""
fi

echo "=========================================="
echo "All test cases completed!"
echo "=========================================="
echo ""
echo "To generate runtime analysis plots, run:"
echo "  1. bash measure_runtime.sh  (measures runtime for all tests)"
echo "  2. python3 plot_runtime.py  (creates visualization plots)"
echo ""
