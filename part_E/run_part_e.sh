#!/bin/bash

# Part E: Comprehensive Test Case Generation and Comparison
# This script generates 1000+ test cases and compares exact vs approximation solutions

set -e  # Exit on error

echo "=========================================="
echo "Part E: Test Case Generation and Comparison"
echo "=========================================="
echo ""

# Step 1: Generate test cases
echo "Step 1: Generating test cases..."
python3 generate_test_cases.py

if [ $? -ne 0 ]; then
    echo "Error: Test case generation failed!"
    exit 1
fi

echo ""
echo "Step 1 complete!"
echo ""

# Step 2: Run comparison
echo "Step 2: Running comparison (this may take a while)..."
python3 run_comparison.py

if [ $? -ne 0 ]; then
    echo "Error: Comparison failed!"
    exit 1
fi

echo ""
echo "Step 2 complete!"
echo ""

# Step 3: Analyze results
echo "Step 3: Analyzing results..."
python3 analyze_comparison.py

if [ $? -ne 0 ]; then
    echo "Error: Analysis failed!"
    exit 1
fi

echo ""
echo "=========================================="
echo "Part E Complete!"
echo "=========================================="
echo ""
echo "Results:"
echo "  - Test cases: part_e_test_cases/"
echo "  - Comparison data: part_e_comparison_results.json"
echo "  - Analysis report: part_e_comparison_report.txt"
echo ""

