#!/usr/bin/env python3
"""
CS 412 Longest Path - Augmented Greedy Approximation (1-Step Lookahead)

This version extends the simple greedy strategy by adding a 1-step lookahead:
For each possible next neighbor, we consider:

    score = weight(current → neighbor) + 
            best(weight neighbor → unvisited node)

The algorithm still tries each vertex as a start, but avoids dead ends and
locally optimal traps better than the basic greedy.
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
        parts = lines[i].split()
        if len(parts) >= 3:
            u, v = parts[0], parts[1]
            w = float(parts[2])
            vertices.add(u)
            vertices.add(v)
            graph[u][v] = w
            graph[v][u] = w
    
    return vertices, graph


def greedy_lookahead_from_start(start, graph, vertices):
    """Greedy longest-path with 1-step lookahead."""
    visited = {start}
    path = [start]
    current = start
    path_length = 0
    
    while True:
        candidates = []

        if current in graph:
            for neighbor, w1 in graph[current].items():
                if neighbor not in visited:
                    
                    # --- 1-Step Lookahead ---
                    best_future = 0
                    if neighbor in graph:
                        for nxt, w2 in graph[neighbor].items():
                            if nxt not in visited and nxt != current:
                                if w2 > best_future:
                                    best_future = w2

                    score = w1 + best_future
                    # Store tuple so tie-breakers fall back to immediate weight
                    candidates.append((score, w1, neighbor))

        if not candidates:
            break

        # Choose the candidate with best score (and best w1 if tie)
        candidates.sort(reverse=True)
        _, chosen_weight, chosen_neighbor = candidates[0]
        
        visited.add(chosen_neighbor)
        path.append(chosen_neighbor)
        path_length += chosen_weight
        current = chosen_neighbor
    
    return path_length, path


def find_longest_path_approx(vertices, graph):
    """Try each vertex as a start and take the best path."""
    if not vertices:
        return 0, []
    
    max_length = 0
    best_path = []
    
    for start in vertices:
        length, path = greedy_lookahead_from_start(start, graph, vertices)
        if length > max_length:
            max_length = length
            best_path = path
    
    return max_length, best_path


def main():
    """Main driver."""
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
