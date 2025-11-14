CS 412 Longest Path - Approximation Solution
=============================================

This folder contains the approximation (polynomial-time) solution for the Longest Path problem.

PROBLEM DESCRIPTION
-------------------
The Longest Path problem finds the longest simple path (no cycles) in an 
undirected weighted graph. This is an NP-complete problem, so we use a 
polynomial-time approximation algorithm that provides a reasonable solution
for large graphs (n > 1000).

ALGORITHM STRATEGY
------------------
The approximation uses a greedy algorithm with random tie-breaking:

1. Try multiple starting vertices (all vertices for small graphs, up to 50 for large)
2. From each starting vertex, greedily extend the path by choosing the 
   highest-weight edge to an unvisited vertex
3. Break ties randomly to add diversity and avoid getting stuck in local optima
4. Return the longest path found across all starting points

This strategy runs in polynomial time O(n * m) where n is vertices and m is edges.

HOW TO RUN
----------
The program can be run in two ways:

1. Read from standard input (for Gradescope):
   python3 cs412_longestpath_approx.py < input_file

2. Read from file:
   python3 cs412_longestpath_approx.py input_file

OPTIONAL COMMAND LINE ARGUMENTS
--------------------------------
--timing          : Output wall clock timing information to stderr
--num-starts N    : Number of starting vertices to try (default: auto)
--seed S          : Random seed for reproducibility

Examples:
  python3 cs412_longestpath_approx.py --timing < input_file
  python3 cs412_longestpath_approx.py --num-starts 100 --seed 42 < input_file

INPUT FORMAT
------------
First line: n m
  - n: number of vertices
  - m: number of edges

Following m lines: u v w
  - u: source vertex name
  - v: destination vertex name  
  - w: edge weight (can be integer or float)

OUTPUT FORMAT
-------------
First line: path_length (as integer)
Second line: space-separated list of vertices in the path

EXAMPLE
-------
Input (test_small_1):
3 3
a b 3
b c 4
a c 5

Output:
9
a c b

This means the approximate longest path has length 9 and follows: a -> c -> b

TEST CASES
----------
Test cases are located in the test_cases/ subfolder:

- test_small_1: Small graph (3 vertices, 3 edges)
- test_small_2: Small graph (4 vertices, 6 edges)
- test_medium_1: Medium graph (5 vertices, 10 edges)
- test_medium_2: Medium graph (6 vertices, 9 edges)
- test_large_1: Large graph (10 vertices, 20 edges)
- test_large_2: Large graph (15 vertices, 30 edges)
- test_very_large: Very large graph (50 vertices, 100 edges) - demonstrates polynomial time
- test_nonoptimal: Graph where approximation may not find optimal solution

To run all test cases:
  bash run_test_cases.sh

To run the non-optimal test case:
  bash run_nonopt_cases.sh

TIME COMPLEXITY
---------------
Worst-case time complexity: O(n * m)
- n: number of vertices
- m: number of edges
- For each starting vertex (up to min(50, n)), we traverse the graph once: O(m)
- Total: O(n * m) which is polynomial time

This allows the algorithm to handle large graphs (n > 1000) efficiently.

SPACE COMPLEXITY
----------------
O(n + m) for graph storage
O(n) for path tracking and visited set

APPROXIMATION QUALITY
---------------------
The greedy algorithm provides good solutions but is not guaranteed to be optimal.
- For many graphs, it finds near-optimal or optimal solutions
- For some graphs, it may find suboptimal solutions
- The random tie-breaking helps avoid getting stuck in poor local optima
- See test_nonoptimal for an example where the approximation may not achieve optimal

EXTERNAL SOURCES
----------------
- Greedy Algorithm Design: Cormen et al., "Introduction to Algorithms" (3rd ed.)
- Approximation Algorithms: Vazirani, "Approximation Algorithms" (2nd ed.)
- Python Standard Library: random, collections, sys modules
- Algorithm design principles from standard CS algorithms textbooks

See approximation_notes.txt for detailed analysis of the approximation strategy,
runtime analysis, and discussion of when it achieves optimal vs suboptimal results.

