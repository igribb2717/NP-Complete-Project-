#!/usr/bin/env python3
"""
CS 412 Longest Path - Approximation Solution
Simple greedy algorithm to find an approximate longest path.

Algorithm: Try each vertex as a starting point, greedily extend the path
by always choosing the highest-weight edge to an unvisited vertex.
Return the longest path found.
"""

import sys
from collections import defaultdict


def read_graph(input_source):
    """Read graph from input file or stdin."""
    if isinstance(input_source, str):
        f = open(input_source, 'r')
        should_close = True
    else:
        f = input_source
        should_close = False
    
    try:
        lines = [line.strip() for line in f if line.strip()]
    finally:
        if should_close:
            f.close()
    
    if not lines:
        return set(), {}
    
    n, m = map(int, lines[0].split())
    graph = defaultdict(dict)
    vertices = set()
    
    for i in range(1, min(m + 1, len(lines))):
        if i >= len(lines):
            break
        parts = lines[i].split()
        if len(parts) >= 3:
            u, v = parts[0], parts[1]
            w = float(parts[2])
            vertices.add(u)
            vertices.add(v)
            graph[u][v] = w
            graph[v][u] = w
    
    return vertices, graph


def greedy_path_from_start(start, graph, vertices):
    """Find a path starting from 'start' using strict greedy strategy."""
    visited = {start}
    path = [start]
    current = start
    path_length = 0
    
    while True:
        candidates = []
        if current in graph:
            for neighbor, weight in graph[current].items():
                if neighbor not in visited:
                    candidates.append((weight, neighbor))
        
        if not candidates:
            break
        
        # Choose the highest weight edge (first one if ties)
        candidates.sort(reverse=True, key=lambda x: x[0])
        chosen_weight, chosen_neighbor = candidates[0]
        
        visited.add(chosen_neighbor)
        path.append(chosen_neighbor)
        path_length += chosen_weight
        current = chosen_neighbor
    
    return path_length, path


def find_longest_path_approx(vertices, graph):
    """Find approximate longest path by trying each vertex as a start."""
    if not vertices:
        return 0, []
    
    max_length = 0
    best_path = []
    
    # Try each vertex as a starting point
    for start in vertices:
        path_length, path = greedy_path_from_start(start, graph, vertices)
        if path_length > max_length:
            max_length = path_length
            best_path = path
    
    return max_length, best_path


def main():
    """Main function."""
    input_source = sys.argv[1] if len(sys.argv) > 1 else sys.stdin
    
    vertices, graph = read_graph(input_source)
    
    if not vertices:
        print(0)
        print()
        return
    
    max_length, best_path = find_longest_path_approx(vertices, graph)
    
    print(f"{int(max_length)}")
    print(" ".join(best_path))


if __name__ == "__main__":
    main()
