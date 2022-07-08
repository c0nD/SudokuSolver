# GUI for SudokuSolver.py

import pygame
from SudokuSolver import solve_sudoku, valid, print_sudoku_board
import time;
pygame.font.init()

class Sudoku_Grid:
    sudoku_board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.squares = [[Square(self.sudoku_board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)] # Sets up each tile
        self.model = None
        self.selected = None

    # Recursively solves itself in the GUI
    def gui_solve(self, window):
        self.update_model()
        found = empty(self.model)
        if not found:
            return True
        else:
            row, col = found

        for i in range(1, 10): # 1-9 inclusive
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.squares[row][col].set(i)
                self.squares[row][col].draw(window)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(75)

                if self.gui_solve(window):
                    return True

                self.model[row][col] = 0
                self.squares[row][col].set(0)
                self.update_model()
                self.squares[row][col].draw(window)
                pygame.display.update()
                pygame.time.delay(75)


    def update_model(self):
        self.model = [[self.squares[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and solve_sudoku(self.model):
                return True
            else:
                self.squares[row][col].set(0)
                self.squares[row][col].set_temp(0)
                self.update_model()
                return False

    # Allows the user to add a temp value/'pencil' it in
    def pencil(self, val):
        row, col = self.selected
        self.squares[row][col].set_temp(val)

    def draw(self, window):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(window, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(window, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Drawing Squares
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(window)

    def clear(self):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_temp(0)

    # @return (row, col)
    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].selected = False

        self.squares[row][col].selected = True
        self.selected = (row, col)

    def is_complete(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].value == 0:
                    return False
        return True


class Square:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.selected = False

    def draw(self, window):
        font = pygame.font.SysFont("ariel", 38)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            window.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            window.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(window, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def render_window(window, board, t, fails):
    # Setup
    window.fill((255, 255, 255))
    font = pygame.font.SysFont("arial", 35)

    # Draw Fails
    text = font.render("X " * fails, 1, (255, 0, 0))
    window.blit(text, (20, 560))
    # Draw time
    text = font.render("Time: " + format_time(t), 1, (0, 0, 0))
    window.blit(text, (380, 560))
    # Draw grid and board
    board.draw(window)


def format_time(sec):
    s = sec % 60
    m = sec // 60
    return str(m) + ":" + str(sec)


def empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None


def main():
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku w/ Autosolver")
    board = Sudoku_Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    fails = 0
    while run:

        delta_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.squares[i][j].temp != 0:
                        if board.place(board.squares[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            fails += 1
                        key = None

                        if board.is_complete():
                            print("GAME. OVER.")
                            run = False

                if event.key == pygame.K_SPACE:
                    board.gui_solve(window)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key:
            board.pencil(key)

        render_window(window, board, delta_time, fails)
        pygame.display.update()


main()
pygame.quit()
