#!/bin/bash

# CS 412 Longest Path - Approximation Solution Test Runner
# This script runs the approximation solution on all test cases

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
echo "CS 412 Longest Path - Approximation Solution Tests"
echo "=========================================="
echo ""

# Check if Python script exists
if [ ! -f "$SCRIPT_DIR/cs412_longestpath_approx.py" ]; then
    echo -e "${RED}Error: cs412_longestpath_approx.py not found!${NC}"
    exit 1
fi

# Function to run test
run_test() {
    local test_name=$1
    local description=$2
    
    echo -e "${GREEN}${description}${NC}"
    echo "  Test file: $test_name"
    echo ""
    
    python3 "$SCRIPT_DIR/cs412_longestpath_approx.py" < "$TEST_DIR/$test_name"
    
    echo ""
    echo "---"
    echo ""
}

# Small test cases
echo -e "${BLUE}=== SMALL TEST CASES ===${NC}"
run_test "test_small_1" "Test 1: Small graph (3 vertices, 3 edges)"
run_test "test_small_2" "Test 2: Small graph (4 vertices, 6 edges)"

# Medium test cases
echo -e "${BLUE}=== MEDIUM TEST CASES ===${NC}"
run_test "test_medium_1" "Test 3: Medium graph (5 vertices, 10 edges)"
run_test "test_medium_2" "Test 4: Medium graph (6 vertices, 9 edges)"

# Large test cases
echo -e "${BLUE}=== LARGE TEST CASES ===${NC}"
run_test "test_large_1" "Test 5: Large graph (10 vertices, 20 edges)"
run_test "test_large_2" "Test 6: Large graph (15 vertices, 30 edges)"

# Very large test case (demonstrates polynomial time performance)
echo -e "${BLUE}=== VERY LARGE TEST CASE (Polynomial Time Performance) ===${NC}"
run_test "test_very_large" "Test 7: Very large graph (50 vertices, 100 edges) - runs in polynomial time"

# Non-optimal test case (where approximation may not achieve optimal)
echo -e "${YELLOW}=== NON-OPTIMAL TEST CASE ===${NC}"
echo -e "${YELLOW}This test case demonstrates that the approximation may not always find the optimal solution.${NC}"
echo -e "${YELLOW}Compare with the exact solution to see the difference.${NC}"
echo ""
run_test "test_nonoptimal" "Test 8: Graph where approximation may be suboptimal"

echo "=========================================="
echo "All test cases completed!"
echo "=========================================="
echo ""
echo "Note: To compare with exact solution, run the exact solver on the same test cases."
echo "The test_nonoptimal case is also available in run_nonopt_cases.sh"

