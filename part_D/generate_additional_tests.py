#!/usr/bin/env python3
"""
Generate additional test cases: 3 examples for each of 8, 9, 10, and 11 vertices.
These will be added to the existing test suite.
"""

import random
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "part_D", "additional_test_cases")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_graph(n, m, weight_range=(1, 100), seed=None):
    """Generate a graph with n vertices and m edges."""
    if seed is not None:
        random.seed(seed)
    
    # Ensure m doesn't exceed maximum possible edges
    max_edges = n * (n - 1) // 2
    if m > max_edges:
        m = max_edges
    
    vertices = [f"v{i}" for i in range(1, n + 1)]
    possible_edges = [(vertices[i], vertices[j]) 
                      for i in range(n) for j in range(i + 1, n)]
    
    selected_edges = random.sample(possible_edges, m)
    edges = [(u, v, random.randint(weight_range[0], weight_range[1])) 
             for u, v in selected_edges]
    
    return vertices, edges


def write_test_case(filename, vertices, edges):
    """Write a test case to a file."""
    n = len(vertices)
    m = len(edges)
    
    with open(filename, 'w') as f:
        f.write(f"{n} {m}\n")
        for u, v, w in edges:
            f.write(f"{u} {v} {w}\n")


def main():
    """Generate 3 test cases for each of 8, 9, 10, and 11 vertices."""
    
    # Test specifications: (vertices, edges_per_test)
    # For each vertex count, we'll create 5 tests with different edge counts
    test_specs = [
        # 8 vertices: max 28 edges
        (8, 12, 1),   # 8v, 12e, test 1
        (8, 16, 2),   # 8v, 16e, test 2
        (8, 20, 3),   # 8v, 20e, test 3
        (8, 14, 4),   # 8v, 14e, test 4 (new)
        (8, 18, 5),   # 8v, 18e, test 5 (new)
        
        # 9 vertices: max 36 edges
        (9, 15, 1),   # 9v, 15e, test 1
        (9, 20, 2),   # 9v, 20e, test 2
        (9, 25, 3),   # 9v, 25e, test 3
        (9, 18, 4),   # 9v, 18e, test 4 (new)
        (9, 22, 5),   # 9v, 22e, test 5 (new)
        
        # 10 vertices: max 45 edges
        (10, 20, 1),  # 10v, 20e, test 1
        (10, 25, 2),  # 10v, 25e, test 2
        (10, 30, 3),  # 10v, 30e, test 3
        (10, 22, 4),  # 10v, 22e, test 4 (new)
        (10, 28, 5),  # 10v, 28e, test 5 (new)
        
        # 11 vertices: max 55 edges
        (11, 25, 1),  # 11v, 25e, test 1
        (11, 35, 2),  # 11v, 35e, test 2
        (11, 45, 3),  # 11v, 45e, test 3
        (11, 30, 4),  # 11v, 30e, test 4 (new)
        (11, 40, 5),  # 11v, 40e, test 5 (new)
    ]
    
    print(f"Generating {len(test_specs)} additional test cases...")
    print(f"Output directory: {OUTPUT_DIR}\n")
    
    for n, m, test_num in test_specs:
        # Use a unique seed for each test
        seed = 5000 + n * 100 + m * 10 + test_num
        vertices, edges = generate_graph(n, m, (1, 100), seed)
        
        filename = os.path.join(OUTPUT_DIR, f"test_{n}v_{test_num}.txt")
        write_test_case(filename, vertices, edges)
        
        print(f"Generated: test_{n}v_{test_num}.txt - {n} vertices, {len(edges)} edges")
    
    print(f"\nGenerated {len(test_specs)} test cases in {OUTPUT_DIR}/")
    print("\nThese will be automatically included when you run:")
    print("  python3 part_D/run_part_D_runtime_study.py")


if __name__ == "__main__":
    main()

