#!/usr/bin/env python3
"""
CS 412 Longest Path - Exact Solution
This program finds the longest simple path in an undirected graph using brute-force.

The longest path problem is NP-complete. This implementation uses a brute-force
approach that explores all possible paths in the graph.

Algorithm:
1. For each vertex as a starting point, perform DFS to explore all possible paths
2. Keep track of the longest path found
3. Return the path with maximum total weight

Time Complexity: O(n! * n) in the worst case, where n is the number of vertices.
This is because we may need to explore all permutations of vertices.

External Sources and References:
---------------------------------
Cursor IDE was used to develop this code 
"""

import sys
from collections import defaultdict


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
    # Start from index 1 (after header) and read up to min(m, available_lines)
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


def find_longest_path(vertices, graph):
    """
    Find the longest simple path in the graph using brute-force DFS.
    
    This function tries all possible paths starting from each vertex.
    It uses backtracking to explore all paths without cycles.
    
    Returns:
        (max_length, best_path): tuple of maximum path length and the path itself
    """
    if not vertices:
        return 0, []
    
    max_length = 0
    best_path = []
    
    # Try each vertex as a starting point
    for start in vertices:
        visited = set()
        current_path = []
        current_length = 0
        
        def dfs(current_vertex, path_length, path):
            """
            Depth-first search to explore all paths from current_vertex.
            
            Args:
                current_vertex: current vertex in the path
                path_length: total weight of the current path
                path: list of vertices in the current path
            """
            nonlocal max_length, best_path
            
            # Update best path if current path is LONGER (maximizing for longest path)
            # This is the LONGEST path problem, so we maximize the path length
            if path_length > max_length:
                max_length = path_length
                best_path = path[:]
            
            # Try all neighbors
            if current_vertex in graph:
                for neighbor, weight in graph[current_vertex].items():
                    if neighbor not in visited:
                        # Add neighbor to path
                        visited.add(neighbor)
                        path.append(neighbor)
                        dfs(neighbor, path_length + weight, path)
                        # Backtrack
                        path.pop()
                        visited.remove(neighbor)
        
        # Start DFS from this vertex
        visited.add(start)
        dfs(start, 0, [start])
        visited.remove(start)
    
    return max_length, best_path


def main():
    """
    Main function to read input, solve longest path, and output result.
    """
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = sys.stdin
    
    vertices, graph = read_graph(input_file)
    
    if not vertices:
        print(0)
        print()
        return
    
    max_length, best_path = find_longest_path(vertices, graph)
    
    # Output: path length on first line, path on second line
    print(f"{int(max_length)}")
    print(" ".join(best_path))


if __name__ == "__main__":
    main()

