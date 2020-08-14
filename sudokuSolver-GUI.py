import time
import pygame
pygame.font.init()

WINDOW = pygame.display.set_mode((600, 690))

# HUD constants
BORDER = 30
BTN_WIDTH = 120
BTN_HEIGHT = 60
BTN_BORDER_WEIGHT = 3
BTN_Y = 600
TEXT_Y = BTN_Y + 12
RESET_BTN_X = BORDER - BTN_WIDTH/2 + 90
SOLVE_BTN_X = 300 - BTN_WIDTH/2
TIME_TEXT_X = BORDER - BTN_WIDTH/2 + 440
RESET_BTN_OFFSET = 18
SOLVE_BTN_OFFSET = 20


class Grid:
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

    def __init__(self, rows, cols, length):
        self.rows = rows
        self.cols = cols
        self.length = length
        self.cellLength = self.length / self.cols
        self.cells = [[Cell(self.board[i][j], i, j, self.cellLength)
                       for j in range(self.cols)] for i in range(self.rows)]
        self.selected = None

    def draw(self):
        # draw the lines
        for i in range(self.rows + 1):
            # make lines that seperate boxes thicker
            if i % 3 == 0:
                weight = 4
            else:
                weight = 1

            pygame.draw.line(WINDOW, (0, 0, 0), (i*self.cellLength + BORDER, BORDER),
                             (i*self.cellLength + BORDER, self.length + BORDER + weight/2), weight)
            pygame.draw.line(WINDOW, (0, 0, 0), (BORDER, i*self.cellLength + BORDER),
                             (self.length + BORDER + weight/2, i*self.cellLength + BORDER), weight)

        # draw the numbers
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw()

    def update(self):
        # update array with the numbers visible on screen
        for i in range(self.rows):
            for j in range(self.cols):
                # ignore incorrect cells on the board
                if self.cells[i][j].fixed:
                    self.board[i][j] = self.cells[i][j].value
                else:
                    self.board[i][j] = 0

    def reset(self):
        # clear all the cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].value = 0
                self.cells[i][j].fixed = False

    def clicked(self, mouseX, mouseY):
        # check if the board was clicked
        if mouseX > BORDER and mouseX < self.length + BORDER and mouseY > BORDER and mouseY < self.length + BORDER:
            return True
        else:
            return False

    def select(self, mouseX, mouseY):
        # determine and select the cell that was clicked
        col = int((mouseX - BORDER) // self.cellLength)
        row = int((mouseY - BORDER) // self.cellLength)

        self.selected = (row, col)
        self.cells[row][col].outlined = True

    def unselectAll(self):
        # remove outline from all cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].outlined = False
        self.selected = None

    def removeSelected(self):
        # delete the value in the selected cell
        row, col = self.selected
        # only can remove cells that are incorrect
        if not self.cells[row][col].fixed:
            self.cells[row][col].value = 0

    def placeNumber(self, num):
        # place a number in the selected cell
        row, col = self.selected

        # only can place a new number in an incorrect cell
        if not self.cells[row][col].fixed:
            # update to the current fixed board
            self.update()

            # add the new number
            self.board[row][col] = num
            self.cells[row][col].value = num

            # if the move is possible and the board is still solvable
            if self.possibleMove(row, col, num) and self.solve():
                self.cells[row][col].fixed = True
            else:
                self.cells[row][col].fixed = False

    def solve(self):
        # find empty spot
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    # try all numbers
                    for num in range(1, 10):
                        if self.possibleMove(row, col, num):
                            self.board[row][col] = num

                            # recursively call solve to go to the next spot
                            if self.solve():
                                return True

                            # backtrack
                            self.board[row][col] = 0
                    # if no numbers are possible, then backtrack to the previous spot
                    return False
        # if no spots are empty, then the board is solved
        return True

    def possibleMove(self, row, col, num):
        # check row
        for i in range(9):
            if self.board[row][i] == num and col != i:
                return False

        # check column
        for i in range(9):
            if self.board[i][col] == num and row != i:
                return False

        # check box
        boxFirstRow = (row // 3) * 3
        boxFirstCol = (col // 3) * 3

        for i in range(3):
            for j in range(3):
                if self.board[boxFirstRow + i][boxFirstCol + j] == num and (row != boxFirstRow + i or col != boxFirstCol + j):
                    return False

        return True

    def solveGUI(self, startTime):
        # find an empty cell
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    # outline the empty cell when it is visited
                    self.cells[row][col].outlined = True

                    # try all numbers
                    for num in range(1, 10):
                        if self.possibleMove(row, col, num):
                            self.board[row][col] = num
                            self.cells[row][col].value = num
                            self.cells[row][col].fixed = True
                            updateWindow(self, startTime)
                            pygame.time.delay(40)

                            # recursively call solve to go to the next cell
                            if self.solveGUI(startTime):
                                return True

                            # backtrack
                            self.board[row][col] = 0
                            self.cells[row][col].value = 'X'
                            self.cells[row][col].fixed = False
                            updateWindow(self, startTime)
                            pygame.time.delay(20)

                    # if no numbers are possible, then backtrack to the previous cell
                    self.cells[row][col].value = 'X'
                    updateWindow(self, startTime)
                    pygame.time.delay(20)
                    return False

        # if no cells are empty, then the board is solved
        self.unselectAll()
        pygame.time.delay(250)
        updateWindow(self, startTime)
        return True


class Cell:
    def __init__(self, value, row, col, length):
        self.value = value
        self.row = row
        self.col = col
        self.length = length
        self.outlined = False
        self.borderColor = (0, 0, 0)
        self.fontColor = (0, 0, 0)

        # determine if the cell is already part of the solution
        if value == 0:
            self.fixed = False
        else:
            self.fixed = True

    def draw(self):
        fnt = pygame.font.SysFont("arial", 38)

        if self.fixed:
            self.fontColor = (0, 0, 0)
            self.borderColor = (0, 255, 0)
        else:
            self.fontColor = (255, 0, 0)
            self.borderColor = (255, 0, 0)

        x = self.col * self.length
        y = self.row * self.length

        # only draw non-empty cells
        if self.value != 0:
            text = fnt.render(str(self.value), 1, self.fontColor)
            offsetX = 0.5 * (self.length - text.get_width()) + BORDER
            offsetY = 0.5 * (self.length - text.get_height()) + BORDER
            WINDOW.blit(text, (x + offsetX, y + offsetY))

        if self.outlined:
            pygame.draw.rect(WINDOW, self.borderColor,
                             (x + BORDER, y + BORDER, self.length + 1, self.length + 1), 4)


def checkResetClick(mouseX, mouseY):
    # check if the reset button was clicked
    if mouseX > RESET_BTN_X and mouseX < RESET_BTN_X + BTN_WIDTH and mouseY > BTN_Y and mouseY < BTN_Y + BTN_HEIGHT:
        return True
    else:
        return False


def checkSolveClick(mouseX, mouseY):
    # check if the solve button was clicked
    if mouseX > SOLVE_BTN_X and mouseX < SOLVE_BTN_X + BTN_WIDTH and mouseY > BTN_Y and mouseY < BTN_Y + BTN_HEIGHT:
        return True
    else:
        return False


def drawHUD(playTime):
    fnt = pygame.font.SysFont("arial", 32)

    # reset button
    pygame.draw.rect(WINDOW, (0, 0, 0), (RESET_BTN_X, BTN_Y,
                                         BTN_WIDTH, BTN_HEIGHT), BTN_BORDER_WEIGHT)
    resetText = fnt.render("Reset", 1, (0, 0, 0))
    WINDOW.blit(resetText, (RESET_BTN_X + RESET_BTN_OFFSET, TEXT_Y))

    # solve button
    pygame.draw.rect(WINDOW, (0, 0, 0), (SOLVE_BTN_X, BTN_Y,
                                         BTN_WIDTH, BTN_HEIGHT), BTN_BORDER_WEIGHT)
    solveText = fnt.render("Solve", 1, (0, 0, 0))
    WINDOW.blit(solveText, (SOLVE_BTN_X + SOLVE_BTN_OFFSET, TEXT_Y))

    # time
    timeText = fnt.render("Time: " + formatTime(playTime), 1, (0, 0, 0))
    WINDOW.blit(timeText, (TIME_TEXT_X, TEXT_Y))


def formatTime(time):
    # format the time to be displayed in the HUD
    seconds = time % 60
    minutes = (time // 60) % 60
    hours = time // 3600
    secPart = ""
    minPart = ""
    hourPart = ""

    # format seconds
    if seconds < 10:
        secPart = ":0" + str(seconds)
    else:
        secPart = ":" + str(seconds)

    # format minutes
    if hours != 0 and minutes < 10:
        minPart = "0" + str(minutes)
    else:
        minPart = str(minutes)

    # format hours
    if hours == 0:
        hourPart = ""
    else:
        hourPart = str(hours) + ":"

    return str(hourPart + minPart + secPart)


def updateWindow(board, startTime):
    playTime = round(time.time() - startTime)
    WINDOW.fill((255, 255, 255))
    board.draw()
    drawHUD(playTime)
    pygame.display.update()


def main():
    # main function with the game loop
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 540)
    startTime = time.time()
    key = None

    running = True
    while running:
        # look for any event
        for event in pygame.event.get():
            # close button
            if event.type == pygame.QUIT:
                running = False
            # mouse pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # get position of the mouse
                pos = pygame.mouse.get_pos()
                mouseX = pos[0]
                mouseY = pos[1]

                board.unselectAll()
                # board
                if board.clicked(mouseX, mouseY):
                    board.select(mouseX, mouseY)
                # reset button
                elif checkResetClick(mouseX, mouseY):
                    startTime = time.time()
                    board.reset()
                # solve button
                elif checkSolveClick(mouseX, mouseY):
                    board.update()
                    board.solveGUI(startTime)
            # key pressed
            elif event.type == pygame.KEYDOWN and board.selected:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9
                elif event.key == pygame.K_DELETE:
                    board.removeSelected()
                    key = None
                else:
                    key = None

                if key != None:
                    board.placeNumber(key)

        updateWindow(board, startTime)


main()
pygame.quit()
