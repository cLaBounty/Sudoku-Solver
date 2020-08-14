"""
@file sudokuSolver-Text.py
@brief A program that uses backtracking to print the solution to any solvable game of sudoku
"""

# initial unsolved board
board = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]
]


def solve(board):
    """
    @brief Solves a sudoku board using backtracking
    @param board: A 2d list of ints that represent a sudoku board
    @return bool: If a solution has been found
    """
    # find empty spot
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                # try all numbers
                for num in range(1, 10):
                    if possible(board, row, col, num):
                        board[row][col] = num

                        # recursively call solve to go to the next spot
                        if solve(board):
                            return True

                        # backtrack
                        board[row][col] = 0
                # if no numbers are possible, then backtrack to the previous spot
                return False
    # if no spots are empty, then the board is solved
    return True


def possible(board, row, col, num):
    """
    @brief Determines if it's possible for a number to go in a spot on the board
    @param board: A 2d list of ints that represent a sudoku board
    @param row: (int) The row of the spot on the board
    @param col: (int) The column of the spot on the board
    @param num: (int) The number to go in the spot
    @return bool: If it's possible for the number to go in the spot on the board
    """
    # check row
    for i in range(9):
        if board[row][i] == num and col != i:
            return False

    # check column
    for i in range(9):
        if board[i][col] == num and row != i:
            return False

    # check box
    boxFirstRow = (row // 3) * 3
    boxFirstCol = (col // 3) * 3

    for i in range(3):
        for j in range(3):
            if board[boxFirstRow + i][boxFirstCol + j] == num and (row != boxFirstRow + i or col != boxFirstCol + j):
                return False

    return True


def printBoard(board):
    """
    @brief Prints a nicely formatted board to the terminal
    @param board: A 2d list of ints that represent a sudoku board
    @return None
    """
    for row in range(len(board)):
        if row % 3 == 0:
            print("  - - - - - - - - - - - - -")

        for col in range(len(board[0])):
            if col % 3 == 0:
                print(" | ", end="")

            print(board[row][col], end="")

            if col == len(board[0]) - 1:
                print(" |", end="\n")
            else:
                print(" ", end="")

    print("  - - - - - - - - - - - - -")


print("Before:")
printBoard(board)

if solve(board):
    print("Solution:")
    printBoard(board)
else:
    print("No Solution")
