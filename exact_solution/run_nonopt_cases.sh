#!/bin/bash

# CS 412 Longest Path - Non-Optimal Test Case Runner
# This script demonstrates a test case where the approximation may not achieve optimal

# Colors for output
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEST_DIR="$SCRIPT_DIR/test_cases"

echo "=========================================="
echo "CS 412 Longest Path - Non-Optimal Test Case"
echo "=========================================="
echo ""
echo -e "${YELLOW}This test case demonstrates that the approximation algorithm${NC}"
echo -e "${YELLOW}may not always find the optimal solution.${NC}"
echo ""

# Check if Python script exists
if [ ! -f "$SCRIPT_DIR/cs412_longestpath_exact.py" ]; then
    echo -e "${RED}Error: cs412_longestpath_exact.py not found!${NC}"
    exit 1
fi

TEST_FILE="$TEST_DIR/test_nonoptimal"

if [ ! -f "$TEST_FILE" ]; then
    echo "Error: test_nonoptimal not found!"
    exit 1
fi

echo -e "${GREEN}Running approximation solution:${NC}"
echo ""
python3 "$SCRIPT_DIR/cs412_longestpath_approx.py" < "$TEST_FILE"
echo ""
echo "---"
echo ""
echo -e "${BLUE}Running exact solution for comparison:${NC}"
echo ""
python3 "$SCRIPT_DIR/cs412_longestpath_exact.py" < "$TEST_FILE"
echo ""
echo "---"
echo ""
echo -e "${YELLOW}Note: If the approximation value is less than the exact value,${NC}"
echo -e "${YELLOW}this demonstrates that the approximation did not achieve optimal.${NC}"

