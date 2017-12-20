CS 271 - Programming Assignment README file
Team: Kyungwoo, Yuya, and Jonathan H
Project: Mastermind

Instead of using Alphabets as colors, we used numbers to calculate. When you input secret code, please convert as follow
  'A' = 0, 'B' = 1, 'C' = 2, ..., 'Y' = 25, 'Z' = 26

To execute the mastermind solver program, simply type:
  (Windows) python .\mastermind-hillclimbing.py <numb. of color> <numb. of post> <secret code>
  (Linux) python mastermind-hillclimbing.py <numb. of color> <numb. of post> <secret code>

Python version: Python v.2.7.13

Example:
  (6 colors 4 pegs case) python .\mastermind-hillclimbing.py 6 4 1 1 2 2

Note:
  This program will automatically create a textfile that contains information
  about the number of guesses and runtime.
  The codes of Genetic Algorithm and Minimax Algorithm are in reference directory.

Benchmark:
  The benchmark result is written in BENCHMARK.txt.
  The last 12 colors 8 positions key: K,K,A,C,L,I,G,F, has possibly get stuck due to
  mutation function continuously generating not arc-consistent guesses.
