#!/bin/bash

# CS 412 Longest Path - Non-Optimal Test Case Runner
# This script demonstrates a test case where the approximation may not achieve optimal

# Colors for output
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEST_DIR="$SCRIPT_DIR/test_cases"
EXACT_DIR="$(dirname "$SCRIPT_DIR")/exact_solution"

echo "=========================================="
echo "CS 412 Longest Path - Non-Optimal Test Case"
echo "=========================================="
echo ""
echo -e "${YELLOW}This test case demonstrates that the approximation algorithm${NC}"
echo -e "${YELLOW}may not always find the optimal solution.${NC}"
echo ""

# Check if Python scripts exist
if [ ! -f "$SCRIPT_DIR/cs412_longestpath_approx.py" ]; then
    echo -e "${RED}Error: cs412_longestpath_approx.py not found!${NC}"
    exit 1
fi

if [ ! -f "$EXACT_DIR/cs412_longestpath_exact.py" ]; then
    echo -e "${RED}Error: cs412_longestpath_exact.py not found in exact_solution!${NC}"
    exit 1
fi

TEST_FILE="$TEST_DIR/test_nonoptimal"

if [ ! -f "$TEST_FILE" ]; then
    echo "Error: test_nonoptimal not found!"
    exit 1
fi

echo -e "${GREEN}Running approximation solution:${NC}"
echo ""
APPROX_OUTPUT=$(python3 "$SCRIPT_DIR/cs412_longestpath_approx.py" < "$TEST_FILE")
echo "$APPROX_OUTPUT"
APPROX_VALUE=$(echo "$APPROX_OUTPUT" | head -1)
echo ""
echo "---"
echo ""
echo -e "${BLUE}Running exact solution for comparison:${NC}"
echo ""
EXACT_OUTPUT=$(python3 "$EXACT_DIR/cs412_longestpath_exact.py" < "$TEST_FILE")
echo "$EXACT_OUTPUT"
EXACT_VALUE=$(echo "$EXACT_OUTPUT" | head -1)
echo ""
echo "---"
echo ""
echo -e "${YELLOW}Results:${NC}"
echo "  Approximation: $APPROX_VALUE"
echo "  Exact (Optimal): $EXACT_VALUE"
echo ""

if [ "$APPROX_VALUE" -lt "$EXACT_VALUE" ]; then
    echo -e "${YELLOW}✓ This demonstrates that the approximation did not achieve optimal.${NC}"
    echo -e "${YELLOW}  The approximation found a path of length $APPROX_VALUE,${NC}"
    echo -e "${YELLOW}  but the optimal solution has length $EXACT_VALUE.${NC}"
else
    echo -e "${GREEN}Note: In this run, the approximation found the optimal solution.${NC}"
    echo -e "${GREEN}Try running multiple times with different seeds to see suboptimal results.${NC}"
fi
