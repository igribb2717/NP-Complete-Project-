CS 412 Longest Path - Exact Solution
=====================================

This folder contains the exact (optimal) solution for the Longest Path problem.

PROBLEM DESCRIPTION
-------------------
The Longest Path problem finds the longest simple path (no cycles) in an 
undirected weighted graph. This is an NP-complete problem, meaning that 
no known polynomial-time algorithm exists to solve it optimally for all cases.

IMPORTANCE AND APPLICATIONS
----------------------------
The Longest Path problem has several important applications:

1. Network Design: Finding the longest path in communication networks to 
   identify critical paths or bottlenecks.

2. Circuit Design: In VLSI design, finding the longest path helps identify 
   critical timing paths that determine circuit performance.

3. Project Scheduling: Similar to critical path method, finding longest paths 
   helps identify tasks that cannot be delayed without affecting project 
   completion time.

4. Bioinformatics: Finding longest paths in protein interaction networks or 
   gene regulatory networks.

5. Transportation Planning: Identifying longest routes for logistics and 
   transportation optimization.

HOW TO RUN
----------
The program can be run in two ways:

1. Read from standard input:
   python3 cs412_longestpath_exact.py < input_file

2. Read from file (if modified to accept filename):
   python3 cs412_longestpath_exact.py input_file

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
Input (test_input_1):
3 3
a b 3
b c 4
a c 5

Output:
9
a c b

This means the longest path has length 9 and follows the path: a -> c -> b
(which uses edges a-c with weight 5 and c-b with weight 4, total = 9)

TEST CASES
----------
Test cases are located in the test_cases/ subfolder, organized by size:

Very Small (< 1 second):
- test_input_small_1: 2 vertices, 1 edge
- test_input_small_2: 3 vertices, 2 edges
- test_input_1: 3 vertices, 3 edges

Small (< 5 seconds):
- test_input_2: 4 vertices, 6 edges
- test_input_3: 5 vertices, 10 edges

Medium (seconds to minutes):
- test_input_4: 6 vertices, 9 edges
- test_input_5: 8 vertices, 12 edges
- test_input_medium_1: 7 vertices, 12 edges
- test_input_6: 10 vertices, 20 edges
- test_input_medium_2: 9 vertices, 15 edges

Large (minutes):
- test_input_7: 12 vertices, 18 edges
- test_input_8: 15 vertices, 30 edges
- test_input_large_1: 11 vertices, 20 edges
- test_input_large_2: 13 vertices, 25 edges

Very Large (> 20 minutes):
- test_input_very_large: 20 vertices, 40 edges
  ** WARNING: This test case takes MORE THAN 20 MINUTES to run **
- test_input_large: 18 vertices, 35 edges
  ** WARNING: This test case takes MORE THAN 20 MINUTES to run **

Extreme (hours):
- test_input_extreme: 22 vertices, 45 edges
  ** WARNING: This test case may take HOURS to run **

To run all test cases, use the provided script:
  bash run_test_cases.sh

RUNTIME ANALYSIS
----------------
To measure and visualize how runtime varies with input size:

1. Measure runtime for all test cases:
   bash measure_runtime.sh
   
   This creates runtime_data.txt with timing information for all tests.

2. Generate visualization plots:
   python3 plot_runtime.py
   
   This creates runtime_analysis.png and runtime_analysis.pdf showing:
   - Runtime vs Number of Vertices
   - Runtime vs Number of Edges
   - Runtime growth on log-log scale
   - Summary table of all test results

The plots clearly illustrate the exponential growth of runtime as input size increases,
demonstrating the NP-complete nature of the problem.

ALGORITHM
---------
The solution uses a brute-force approach with backtracking:
1. Try each vertex as a starting point
2. For each starting vertex, perform depth-first search (DFS) to explore 
   all possible paths
3. Keep track of the longest path found
4. Return the path with maximum total weight

TIME COMPLEXITY
---------------
Worst-case time complexity: O(n! * n)
- n! possible paths to explore (all permutations of vertices)
- n operations per path to calculate length

This exponential complexity makes the problem intractable for large graphs,
which is why it is NP-complete.

SPACE COMPLEXITY
----------------
O(n + m) for graph storage
O(n) for recursion stack and path tracking

EXTERNAL SOURCES
----------------
- Longest Path Problem: https://en.wikipedia.org/wiki/Longest_path_problem
- NP-Completeness: Garey & Johnson, "Computers and Intractability: A Guide 
  to the Theory of NP-Completeness"
- Algorithm design principles from standard CS algorithms textbooks

