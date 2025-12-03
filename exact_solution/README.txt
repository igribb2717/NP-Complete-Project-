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

SMALL TEST CASES - CORRECTNESS VERIFICATION
--------------------------------------------
The following small test cases are documented to demonstrate the correctness
of the exact solution. Each test case shows the input, output, and verification
that the solution finds the optimal longest path.

Test Case 1: test_input_small_1 (2 vertices, 1 edge)
----------------------------------------------------
Input:
  2 1
  a b 5

Output:
  5
  b a

Verification:
  - Graph has only 2 vertices (a, b) with 1 edge of weight 5
  - The longest path must use the only edge: a-b (or b-a)
  - Path length = 5 (correct)
  - The solution correctly identifies this trivial case

Test Case 2: test_input_small_2 (3 vertices, 2 edges)
------------------------------------------------------
Input:
  3 2
  a b 3
  b c 4

Output:
  7
  a b c

Verification:
  - Graph: a--3--b--4--c (linear chain)
  - Possible paths:
    * a->b->c: weight = 3 + 4 = 7
    * a->b: weight = 3
    * b->c: weight = 4
  - Longest path: a->b->c with length 7 (correct)
  - The solution correctly finds the path that uses both edges

Test Case 3: test_input_1 (3 vertices, 3 edges - triangle)
------------------------------------------------------------
Input:
  3 3
  a b 3
  b c 4
  a c 5

Output:
  9
  a c b

Verification:
  - Graph is a triangle (complete graph on 3 vertices)
  - All possible paths:
    * a->b->c: weight = 3 + 4 = 7
    * a->c->b: weight = 5 + 4 = 9  ← OPTIMAL
    * b->a->c: weight = 3 + 5 = 8
    * b->c->a: weight = 4 + 5 = 9  ← OPTIMAL (alternative)
    * c->a->b: weight = 5 + 3 = 8
    * c->b->a: weight = 4 + 3 = 7
  - Longest path: a->c->b (or b->c->a) with length 9 (correct)
  - The solution correctly chooses the path using the two heaviest edges (5 and 4)

Test Case 4: test_input_2 (4 vertices, 6 edges - complete graph K4)
--------------------------------------------------------------------
Input:
  4 6
  a b 1
  a c 2
  a d 3
  b c 4
  b d 5
  c d 6

Output:
  13
  b c d a

Verification:
  - Graph is a complete graph on 4 vertices (K4)
  - The longest path must visit all 4 vertices (maximum length for 4 vertices)
  - Path b->c->d->a: weight = 4 + 6 + 3 = 13
  - Alternative optimal paths:
    * c->d->a->b: weight = 6 + 3 + 1 = 10 (not optimal)
    * d->c->b->a: weight = 6 + 4 + 1 = 11 (not optimal)
    * b->d->c->a: weight = 5 + 6 + 2 = 13 (also optimal)
  - The solution correctly finds a path of length 13, which is optimal
  - Verification: The path uses edges (b-c:4), (c-d:6), (d-a:3) = 13
  - No path visiting all 4 vertices can exceed 13, confirming optimality

Correctness Summary:
--------------------
These small test cases demonstrate that the exact solution:
1. Handles trivial cases (2 vertices) correctly
2. Finds paths in linear chains correctly
3. Chooses optimal paths when multiple options exist (triangle case)
4. Finds optimal paths in complete graphs (K4 case)
5. Correctly calculates path lengths by summing edge weights
6. Returns valid paths (no cycles, all edges exist in the graph)

The solution's correctness on these small, verifiable cases provides confidence
that the algorithm correctly implements the longest path problem for larger inputs.

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

