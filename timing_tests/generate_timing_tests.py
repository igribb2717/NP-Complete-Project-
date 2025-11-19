#!/usr/bin/env python3
"""
Generate test cases for timing tests.
Creates 10 test cases starting at 10 vertices and 45 edges,
progressing to 14 vertices and 80 edges.
Note: 12 vertices can have at most 66 edges, so we increase vertices
to reach 80 edges as requested.
"""

import random
import os

def generate_sparse_graph(n, m, weight_range=(1, 100), seed=None):
    """Generate a sparse graph with n vertices and m edges."""
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
    """Generate 10 test cases for timing tests."""
    output_dir = os.path.dirname(os.path.abspath(__file__))
    test_dir = os.path.join(output_dir, "test_cases")
    os.makedirs(test_dir, exist_ok=True)
    
    # Test case specifications: (vertices, edges)
    # Note: For an undirected graph with n vertices, max edges = n*(n-1)/2
    # 10 vertices max = 45 edges, 11 vertices max = 55 edges, 12 vertices max = 66 edges
    # To reach 80 edges, we need at least 13 vertices (13 vertices max = 78 edges)
    # So we use 14 vertices for the final test to reach 80 edges
    test_specs = [
        (10, 45),  # Test 1: 10 vertices, max 45 edges (closest to requested 60)
        (11, 50),  # Test 2: 11 vertices
        (11, 55),  # Test 3: 11 vertices, max 55 edges
        (12, 60),  # Test 4: 12 vertices, 60 edges (as requested)
        (12, 66),  # Test 5: 12 vertices, max 66 edges
        (13, 70),  # Test 6: 13 vertices
        (13, 75),  # Test 7: 13 vertices
        (13, 78),  # Test 8: 13 vertices, max 78 edges
        (14, 80),  # Test 9: 14 vertices, 80 edges (as requested)
        (14, 80),  # Test 10: 14 vertices, 80 edges
    ]
    
    print("Generating timing test cases...")
    for i, (n, m) in enumerate(test_specs, 1):
        # Use a consistent seed for reproducibility, but different for each test
        seed = 1000 + i
        vertices, edges = generate_sparse_graph(n, m, (1, 100), seed)
        
        # Ensure we have exactly m edges (in case it was adjusted)
        actual_m = len(edges)
        if actual_m != m:
            print(f"Warning: Test {i} requested {m} edges but got {actual_m} (max possible: {n * (n - 1) // 2})")
        
        filename = os.path.join(test_dir, f"test_{i:02d}.txt")
        write_test_case(filename, vertices, edges)
        print(f"Generated test_{i:02d}.txt: {n} vertices, {actual_m} edges")
    
    print(f"\nGenerated {len(test_specs)} test cases in {test_dir}/")

if __name__ == "__main__":
    main()

