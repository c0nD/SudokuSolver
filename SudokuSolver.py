"""
Author: c0nD
Version: 1.0.0

Uses a backtracking algorithm to recursively solve a given sudoku board.
"""


def solve_sudoku(board):
    found = find_empty(board)  # Finds empty slots (0)
    if not found:
        return True
    else:
        row, col = found

    for i in range(1,10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False


def valid(board, num, position):
    # Checks the row for validity
    for i in range(len(board[0])):
        if board[position[0]][i] == num and position[1] != i:
            return False

    # Checks the column for validity
    for i in range(len(board)):
        if board[i][position[1]] == num and position[0] != i:
            return False

    # Shows what 3x3 box we land in
    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == num and (i,j) != position:
                return False

    return True


def print_sudoku_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("-=-=-=-=-=-=-=-=-=-=-=-")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(f'{board[i][j]}' + " ", end="")


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None
