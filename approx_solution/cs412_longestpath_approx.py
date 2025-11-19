#!/usr/bin/env python3
"""
CS 412 Longest Path - Approximation Solution
This program finds an approximate longest simple path in an undirected graph using a greedy algorithm.

The algorithm uses a greedy strategy with random tie-breaking to find a long path in polynomial time.
It tries multiple starting vertices and selects the best path found.

Algorithm Strategy:
1. Try multiple starting vertices (or all vertices for small graphs)
2. From each start, greedily extend the path by choosing the highest-weight edge to an unvisited vertex
3. Break ties randomly to add diversity
4. Return the longest path found across all attempts

Time Complexity: O(n * m) where n is vertices and m is edges - polynomial time
Space Complexity: O(n + m)

"""

import sys
import random
from collections import defaultdict
import argparse
import time


def read_graph(input_source):
    """
    Read graph from input file or stdin.
    Format: First line has n (vertices) and m (edges)
    Following m lines have: u v w (edge from u to v with weight w)
    
    Args:
        input_source: either a file path (string) or file-like object (stdin)
    
    Returns:
        vertices: set of vertex names
        graph: dictionary mapping (u, v) -> weight (undirected, so both directions stored)
    """
    # Handle both file path and stdin
    if isinstance(input_source, str):
        f = open(input_source, 'r')
        should_close = True
    else:
        f = input_source
        should_close = False
    
    try:
        # Read all lines, filtering out empty lines
        lines = [line.strip() for line in f if line.strip()]
    finally:
        if should_close:
            f.close()
    
    if not lines:
        return set(), {}
    
    n, m = map(int, lines[0].split())
    graph = defaultdict(dict)
    vertices = set()
    
    # Read edges - only read as many as are available (in case file has fewer than m)
    num_available_edges = len(lines) - 1  # Subtract 1 for header line
    num_edges_to_read = min(m, num_available_edges)
    
    for i in range(1, num_edges_to_read + 1):
        if i >= len(lines):
            break  # Safety check
        parts = lines[i].split()
        if len(parts) >= 3:
            u, v = parts[0], parts[1]
            w = float(parts[2])
            vertices.add(u)
            vertices.add(v)
            # Store edge in both directions (undirected graph)
            graph[u][v] = w
            graph[v][u] = w
    
    return vertices, graph


def greedy_path_from_start(start, graph, vertices, random_seed=None, strategy='greedy'):
    """
    Find a path starting from 'start' using a greedy strategy.
    
    At each step, chooses the highest-weight edge to an unvisited vertex.
    Breaks ties randomly.
    
    Args:
        start: starting vertex
        graph: adjacency dictionary
        vertices: set of all vertices
        random_seed: optional seed for reproducibility
        strategy: 'greedy' (simple greedy) or 'lookahead' (prefer vertices with high-weight edges)
    
    Returns:
        (path_length, path): tuple of path length and list of vertices
    """
    if random_seed is not None:
        random.seed(random_seed)
    
    visited = {start}
    path = [start]
    current = start
    path_length = 0
    
    while True:
        # Find all unvisited neighbors with their edge weights
        candidates = []
        if current in graph:
            for neighbor, weight in graph[current].items():
                if neighbor not in visited:
                    if strategy == 'lookahead':
                        # Score based on edge weight + potential future edges
                        # Look at the maximum edge weight from this neighbor to unvisited vertices
                        future_potential = 0
                        if neighbor in graph:
                            for future_neighbor, future_weight in graph[neighbor].items():
                                if future_neighbor not in visited and future_neighbor != current:
                                    future_potential = max(future_potential, future_weight)
                        # Combine current edge weight with potential (weighted)
                        score = weight + 0.3 * future_potential
                        candidates.append((score, weight, neighbor))
                    else:
                        candidates.append((weight, weight, neighbor))
        
        if not candidates:
            break  # No more neighbors to visit
        
        # Sort by score (descending), then randomly shuffle ties
        candidates.sort(reverse=True, key=lambda x: x[0])
        
        # Find all candidates with the maximum score (ties)
        max_score = candidates[0][0]
        tied_candidates = [c for c in candidates if abs(c[0] - max_score) < 1e-9]
        
        # Randomly choose among tied candidates
        _, chosen_weight, chosen_neighbor = random.choice(tied_candidates)
        
        # Add to path
        visited.add(chosen_neighbor)
        path.append(chosen_neighbor)
        path_length += chosen_weight
        current = chosen_neighbor
    
    return path_length, path


def find_longest_path_approx(vertices, graph, num_starts=None, random_seed=None):
    """
    Find an approximate longest path using greedy algorithm with multiple starting points.
    
    Args:
        vertices: set of all vertices
        graph: adjacency dictionary
        num_starts: number of starting vertices to try (None = try all for small graphs, 
                   or more for large graphs)
        random_seed: optional seed for reproducibility
    
    Returns:
        (max_length, best_path): tuple of maximum path length and the path itself
    """
    if not vertices:
        return 0, []
    
    n = len(vertices)
    
    # Determine how many starting vertices to try
    if num_starts is None:
        # Try all vertices for small/medium graphs, more for large graphs
        if n <= 100:
            num_starts = n  # Try all vertices
        elif n <= 200:
            num_starts = min(150, n)  # Try most vertices
        else:
            num_starts = min(200, n)  # Try up to 200 for very large graphs
    
    # Select starting vertices
    vertex_list = list(vertices)
    if num_starts >= n:
        starts = vertex_list
    else:
        # Randomly sample starting vertices
        if random_seed is not None:
            random.seed(random_seed)
        starts = random.sample(vertex_list, num_starts)
    
    max_length = 0
    best_path = []
    
    # Number of random seeds to try per starting vertex
    # More seeds = more diversity in tie-breaking, better chance of finding good paths
    if n <= 20:
        num_seeds_per_start = 30  # Small graphs: try many seeds
    elif n <= 50:
        num_seeds_per_start = 20  # Medium graphs: try many seeds
    elif n <= 100:
        num_seeds_per_start = 15  # Larger graphs: still try many seeds
    else:
        num_seeds_per_start = 10  # Very large graphs: limit seeds to keep polynomial
    
    # Try each starting vertex with multiple random seeds and strategies
    for i, start in enumerate(starts):
        # Try multiple random seeds for this starting vertex
        for seed_offset in range(num_seeds_per_start):
            # Use different seed for each attempt
            if random_seed is not None:
                seed = random_seed + i * 1000 + seed_offset
            else:
                seed = i * 1000 + seed_offset
            
            # Try simple greedy strategy
            path_length, path = greedy_path_from_start(start, graph, vertices, seed, strategy='greedy')
            if path_length > max_length:
                max_length = path_length
                best_path = path
            
            # Try lookahead strategy (prefer vertices with high-weight future edges)
            path_length, path = greedy_path_from_start(start, graph, vertices, seed, strategy='lookahead')
            if path_length > max_length:
                max_length = path_length
                best_path = path
    
    return max_length, best_path


def main():
    """
    Main function to read input, solve longest path approximation, and output result.
    """
    parser = argparse.ArgumentParser(description='Longest Path Approximation Solver')
    parser.add_argument('--timing', action='store_true', 
                       help='Output wall clock timing information')
    parser.add_argument('--num-starts', type=int, default=None,
                       help='Number of starting vertices to try (default: auto)')
    parser.add_argument('--seed', type=int, default=None,
                       help='Random seed for reproducibility')
    parser.add_argument('input_file', nargs='?', default=None,
                       help='Input file (if not provided, reads from stdin)')
    
    args = parser.parse_args()
    
    # Read input
    if args.input_file:
        input_source = args.input_file
    else:
        input_source = sys.stdin
    
    start_time = time.time()
    
    vertices, graph = read_graph(input_source)
    
    if not vertices:
        print(0)
        print()
        if args.timing:
            elapsed = time.time() - start_time
            print(f"# Runtime: {elapsed:.4f} seconds", file=sys.stderr)
        return
    
    max_length, best_path = find_longest_path_approx(
        vertices, graph, 
        num_starts=args.num_starts,
        random_seed=args.seed
    )
    
    elapsed = time.time() - start_time
    
    # Output: path length on first line, path on second line
    print(f"{int(max_length)}")
    print(" ".join(best_path))
    
    if args.timing:
        print(f"# Runtime: {elapsed:.4f} seconds", file=sys.stderr)


if __name__ == "__main__":
    main()

