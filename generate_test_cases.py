#!/usr/bin/env python3
"""
Test Case Generator for Longest Path Problem
Generates 1000+ diverse test cases to compare exact vs approximation solutions.

Test case types:
1. Small graphs (3-5 vertices) - many cases
2. Medium graphs (6-8 vertices) - many cases  
3. Larger graphs (9-12 vertices) - fewer cases (exact solution slower)
4. Sparse graphs (tree-like, few edges)
5. Dense graphs (many edges)
6. Graphs designed to trick greedy algorithms
7. Random graphs with various properties
"""

import random
import os
import itertools
from collections import defaultdict

def generate_complete_graph(n, weight_range=(1, 100), seed=None):
    """Generate a complete graph with n vertices."""
    if seed is not None:
        random.seed(seed)
    
    vertices = [f"v{i}" for i in range(1, n + 1)]
    edges = []
    
    for i in range(n):
        for j in range(i + 1, n):
            weight = random.randint(weight_range[0], weight_range[1])
            edges.append((vertices[i], vertices[j], weight))
    
    return vertices, edges

def generate_tree_graph(n, weight_range=(1, 100), seed=None):
    """Generate a tree (n-1 edges, no cycles)."""
    if seed is not None:
        random.seed(seed)
    
    vertices = [f"v{i}" for i in range(1, n + 1)]
    edges = []
    used = {vertices[0]}
    
    for i in range(1, n):
        u = random.choice(list(used))
        v = vertices[i]
        weight = random.randint(weight_range[0], weight_range[1])
        edges.append((u, v, weight))
        used.add(v)
    
    return vertices, edges

def generate_path_graph(n, weight_range=(1, 100), seed=None):
    """Generate a simple path graph."""
    if seed is not None:
        random.seed(seed)
    
    vertices = [f"v{i}" for i in range(1, n + 1)]
    edges = []
    
    for i in range(n - 1):
        weight = random.randint(weight_range[0], weight_range[1])
        edges.append((vertices[i], vertices[i + 1], weight))
    
    return vertices, edges

def generate_cycle_graph(n, weight_range=(1, 100), seed=None):
    """Generate a cycle graph."""
    if seed is not None:
        random.seed(seed)
    
    vertices = [f"v{i}" for i in range(1, n + 1)]
    edges = []
    
    for i in range(n):
        weight = random.randint(weight_range[0], weight_range[1])
        edges.append((vertices[i], vertices[(i + 1) % n], weight))
    
    return vertices, edges

def generate_sparse_graph(n, m, weight_range=(1, 100), seed=None):
    """Generate a sparse graph with n vertices and m edges."""
    if seed is not None:
        random.seed(seed)
    
    if m > n * (n - 1) // 2:
        m = n * (n - 1) // 2
    
    vertices = [f"v{i}" for i in range(1, n + 1)]
    possible_edges = [(vertices[i], vertices[j]) 
                      for i in range(n) for j in range(i + 1, n)]
    
    selected_edges = random.sample(possible_edges, m)
    edges = [(u, v, random.randint(weight_range[0], weight_range[1])) 
             for u, v in selected_edges]
    
    return vertices, edges

def generate_dense_graph(n, density=0.7, weight_range=(1, 100), seed=None):
    """Generate a dense graph with given density."""
    if seed is not None:
        random.seed(seed)
    
    max_edges = n * (n - 1) // 2
    m = int(max_edges * density)
    return generate_sparse_graph(n, m, weight_range, seed)

def generate_greedy_trap_graph(n, seed=None):
    """
    Generate a graph designed to trick greedy algorithms.
    Creates a structure where greedy choice early leads to suboptimal path.
    """
    if seed is not None:
        random.seed(seed)
    
    vertices = [f"v{i}" for i in range(1, n + 1)]
    edges = []
    
    # Create a structure: start -> high-weight edge -> dead end
    # vs start -> medium edges -> longer path with more total weight
    if n >= 4:
        # High weight edge that looks attractive but leads to dead end
        edges.append((vertices[0], vertices[1], 100))
        edges.append((vertices[1], vertices[2], 1))  # Dead end
        
        # Alternative path: multiple medium edges that sum to more
        edges.append((vertices[0], vertices[3], 30))
        for i in range(3, min(n, 6)):
            if i + 1 < n:
                edges.append((vertices[i], vertices[i + 1], 30))
        
        # Add more connections to make it interesting
        for i in range(4, n):
            for j in range(i + 1, min(i + 3, n)):
                weight = random.randint(10, 50)
                edges.append((vertices[i], vertices[j], weight))
    
    return vertices, edges

def generate_star_graph(n, weight_range=(1, 100), seed=None):
    """Generate a star graph (one central vertex connected to all others)."""
    if seed is not None:
        random.seed(seed)
    
    vertices = [f"v{i}" for i in range(1, n + 1)]
    edges = []
    
    center = vertices[0]
    for i in range(1, n):
        weight = random.randint(weight_range[0], weight_range[1])
        edges.append((center, vertices[i], weight))
    
    return vertices, edges

def generate_bipartite_graph(n1, n2, m, weight_range=(1, 100), seed=None):
    """Generate a bipartite graph."""
    if seed is not None:
        random.seed(seed)
    
    vertices1 = [f"a{i}" for i in range(1, n1 + 1)]
    vertices2 = [f"b{i}" for i in range(1, n2 + 1)]
    vertices = vertices1 + vertices2
    
    possible_edges = [(u, v) for u in vertices1 for v in vertices2]
    if m > len(possible_edges):
        m = len(possible_edges)
    
    selected_edges = random.sample(possible_edges, m)
    edges = [(u, v, random.randint(weight_range[0], weight_range[1])) 
             for u, v in selected_edges]
    
    return vertices, edges

def generate_random_graph(n, m, weight_range=(1, 100), seed=None):
    """Generate a random graph."""
    return generate_sparse_graph(n, m, weight_range, seed)

def write_test_case(filename, vertices, edges):
    """Write a test case to a file."""
    n = len(vertices)
    m = len(edges)
    
    with open(filename, 'w') as f:
        f.write(f"{n} {m}\n")
        for u, v, w in edges:
            f.write(f"{u} {v} {w}\n")

def main():
    """Generate 1000+ test cases."""
    output_dir = "part_e_test_cases"
    os.makedirs(output_dir, exist_ok=True)
    
    test_count = 0
    random.seed(42)  # For reproducibility
    
    print("Generating test cases...")
    
    # 1. Small graphs (3-5 vertices) - 350 cases
    print("Generating small graphs (3-5 vertices)...")
    for size in [3, 4, 5]:
        for i in range(117):
            # Complete graphs
            if i % 10 == 0:
                vertices, edges = generate_complete_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Trees
            if i % 10 == 1:
                vertices, edges = generate_tree_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Paths
            if i % 10 == 2:
                vertices, edges = generate_path_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Cycles
            if i % 10 == 3 and size >= 3:
                vertices, edges = generate_cycle_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Sparse graphs
            if i % 10 in [4, 5]:
                m = random.randint(size - 1, size * 2)
                vertices, edges = generate_sparse_graph(size, m, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Dense graphs
            if i % 10 in [6, 7]:
                density = random.uniform(0.5, 0.9)
                vertices, edges = generate_dense_graph(size, density, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Greedy trap graphs
            if i % 10 == 8:
                vertices, edges = generate_greedy_trap_graph(size, test_count)
                if len(edges) > 0:
                    write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                    test_count += 1
            
            # Random graphs
            if i % 10 == 9:
                max_edges = size * (size - 1) // 2
                m = random.randint(size - 1, max_edges)
                vertices, edges = generate_random_graph(size, m, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
    
    # 2. Medium graphs (6-8 vertices) - 450 cases
    print("Generating medium graphs (6-8 vertices)...")
    for size in [6, 7, 8]:
        for i in range(150):
            # Complete graphs (fewer, as they're larger)
            if i % 20 == 0:
                vertices, edges = generate_complete_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Trees
            if i % 20 in [1, 2]:
                vertices, edges = generate_tree_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Paths
            if i % 20 == 3:
                vertices, edges = generate_path_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Cycles
            if i % 20 == 4:
                vertices, edges = generate_cycle_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Sparse graphs
            if i % 20 in [5, 6, 7, 8]:
                m = random.randint(size, size * 2)
                vertices, edges = generate_sparse_graph(size, m, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Dense graphs
            if i % 20 in [9, 10, 11]:
                density = random.uniform(0.4, 0.8)
                vertices, edges = generate_dense_graph(size, density, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Greedy trap graphs (important for showing approximation failures)
            if i % 20 in [12, 13, 14]:
                vertices, edges = generate_greedy_trap_graph(size, test_count)
                if len(edges) > 0:
                    write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                    test_count += 1
            
            # Star graphs
            if i % 20 == 15:
                vertices, edges = generate_star_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Bipartite graphs
            if i % 20 == 16:
                n1 = size // 2
                n2 = size - n1
                m = random.randint(n1 + n2 - 1, n1 * n2)
                vertices, edges = generate_bipartite_graph(n1, n2, m, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Random graphs
            if i % 20 in [17, 18, 19]:
                max_edges = size * (size - 1) // 2
                m = random.randint(size, max_edges)
                vertices, edges = generate_random_graph(size, m, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
    
    # 3. Larger graphs (9-12 vertices) - 300 cases (fewer complete graphs)
    print("Generating larger graphs (9-12 vertices)...")
    for size in [9, 10, 11, 12]:
        for i in range(75):
            # Trees (fast for exact solution)
            if i % 10 in [0, 1]:
                vertices, edges = generate_tree_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Paths
            if i % 10 == 2:
                vertices, edges = generate_path_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Cycles
            if i % 10 == 3:
                vertices, edges = generate_cycle_graph(size, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Sparse graphs
            if i % 10 in [4, 5, 6]:
                m = random.randint(size, size * 2)
                vertices, edges = generate_sparse_graph(size, m, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Dense graphs (fewer, as exact solution is slow)
            if i % 10 == 7:
                density = random.uniform(0.3, 0.6)
                vertices, edges = generate_dense_graph(size, density, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
            
            # Greedy trap graphs
            if i % 10 == 8:
                vertices, edges = generate_greedy_trap_graph(size, test_count)
                if len(edges) > 0:
                    write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                    test_count += 1
            
            # Random graphs
            if i % 10 == 9:
                max_edges = size * (size - 1) // 2
                m = random.randint(size, min(max_edges, size * 3))
                vertices, edges = generate_random_graph(size, m, (1, 100), test_count)
                write_test_case(f"{output_dir}/test_{test_count:04d}.txt", vertices, edges)
                test_count += 1
    
    print(f"\nGenerated {test_count} test cases in {output_dir}/")
    print(f"Test cases range from test_0000.txt to test_{test_count-1:04d}.txt")

if __name__ == "__main__":
    main()

