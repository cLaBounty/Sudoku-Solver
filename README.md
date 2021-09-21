# Sudoku Solver

### [Demo](https://www.youtube.com/watch?v=mpyLjhE6kZ0) | [Download](https://clabounty.itch.io/sudoku-solver)

## Summary
A Sudoku game and solver that uses a backtracking algorithm to find a solution to any solvable game. Added functionality to play the game as well as manually input your own board. Built in Python using the Pygame library.

## The Solving Method
The solving method that I chose to implement uses backtracking. Backtracking is when you revert back to the previous step or solution as soon as it is determined that the current solution cannot be continued into a complete one. The algorithm starts by finding an empty spot on the board and attempts to put all numbers (1-9) in that spot. It then checks each number to see if it is possible to put it in that spot by seeing if there is already the same number in that row, column, or box. If a possible number is found, then put that number in the spot, and recursively attempt to fill the next empty spot of the board. If a possible number is not found, then backtrack to the previous spot, reset it, and continue to look for a different possible number. When there are no empty spots left on the board, then the algorithm arrives at the base case, and the board is solved.

## How it was Built
For this project, I first built a text version in Python that takes a Suduko board, represented by a 2D list of integers, and prints a nicely formatted solved board to the terminal. I then decided that I wanted to create a GUI version using Pygame where the backtracking algorithm used to solve the board could be visualized. The algorithm used for the text version could also be applied to the GUI version and I simply modified and updated the board during different parts of the algorithm. For example, when a possible number is found for an empty cell, it gets filled with that number and a green outline. When there isn't a possible number for an empty cell and the algorithm backtracks, then the cell without any possibilities gets filled with an 'X' and a red outline. After implementing the solving visualization, I decided that I wanted to add functionality to play the game as well as manually input your own board. These both involve entering a number on the board, which can only be done when the number can possibly be put in the cell and the board can still be solved with the number in the cell.

## What I Learned
- Python Syntax and Keywords
- Pygame Library
- Backtracking Algorithm
