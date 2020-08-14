import time
import pygame
pygame.font.init()

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

WINDOW = pygame.display.set_mode((600, 690))


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

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cellLength = self.width / self.cols
        self.cells = [[Cell(self.board[i][j], i, j, self.cellLength)
                       for j in range(self.cols)] for i in range(self.rows)]
        self.selected = None

    def update(self):
        for row in range(self.rows):
            for col in range(self.cols):
                # ignore incorrect cells on the board
                if self.cells[row][col].fixed:
                    self.board[row][col] = self.cells[row][col].value
                else:
                    self.board[row][col] = 0

    def reset(self):
        # clear all cells
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].value = 0
                self.cells[row][col].fixed = False

    def draw(self):
        # draw lines
        for i in range(self.rows + 1):
            if i % 3 == 0:
                weight = 4
            else:
                weight = 1

            pygame.draw.line(WINDOW, (0, 0, 0), (i*self.cellLength + BORDER, BORDER),
                             (i*self.cellLength + BORDER, self.height + BORDER + weight/2), weight)
            pygame.draw.line(WINDOW, (0, 0, 0), (BORDER, i*self.cellLength + BORDER),
                             (self.width + BORDER + weight/2, i*self.cellLength + BORDER), weight)

        # draw numbers in cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw()

    def clicked(self, mouseX, mouseY):
        if mouseX > BORDER and mouseX < self.width + BORDER and mouseY > BORDER and mouseY < self.height + BORDER:
            return True
        else:
            return False

    def select(self, mouseX, mouseY):
        # select the clicked cell
        col = int((mouseX - BORDER) // self.cellLength)
        row = int((mouseY - BORDER) // self.cellLength)

        self.selected = (row, col)
        self.cells[row][col].outlined = True

    def unselectAll(self):
        # unselect all cells
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].outlined = False
        self.selected = None

    def removeSelected(self):
        row, col = self.selected
        # only can remove incorrect cells
        if not self.cells[row][col].fixed:
            self.cells[row][col].value = 0

    def placeNumber(self, num):
        row, col = self.selected

        if not self.cells[row][col].fixed:
            # update to the current fixed board
            self.update()

            # add the new number
            self.board[row][col] = num
            self.cells[row][col].value = num

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

    def solveGUI(self, playTime):
        # find empty spot
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    self.cells[row][col].outlined = True

                    # try all numbers
                    for num in range(1, 10):
                        if self.possibleMove(row, col, num):
                            self.board[row][col] = num
                            self.cells[row][col].value = num
                            self.cells[row][col].fixed = True
                            updateWindow(self, playTime)
                            pygame.time.delay(40)

                            # recursively call solve to go to the next spot
                            if self.solveGUI(playTime):
                                return True

                            # backtrack
                            self.board[row][col] = 0
                            self.cells[row][col].value = 'X'
                            self.cells[row][col].fixed = False
                            updateWindow(self, playTime)
                            pygame.time.delay(20)

                    # if no numbers are possible, then backtrack to the previous spot
                    self.cells[row][col].value = 'X'
                    updateWindow(self, playTime)
                    pygame.time.delay(20)
                    return False

        # if no spots are empty, then the board is solved
        self.unselectAll()
        pygame.time.delay(250)
        updateWindow(self, playTime)
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

        # only draw filled cells
        if self.value != 0:
            text = fnt.render(str(self.value), 1, self.fontColor)
            offsetX = 0.5 * (self.length - text.get_width()) + BORDER
            offsetY = 0.5 * (self.length - text.get_height()) + BORDER
            WINDOW.blit(text, (x + offsetX, y + offsetY))

        if self.outlined:
            pygame.draw.rect(WINDOW, self.borderColor,
                             (x + BORDER, y + BORDER, self.length + 1, self.length + 1), 4)


def checkResetClick(mouseX, mouseY):
    if mouseX > RESET_BTN_X and mouseX < RESET_BTN_X + BTN_WIDTH and mouseY > BTN_Y and mouseY < BTN_Y + BTN_HEIGHT:
        return True
    else:
        return False


def checkSolveClick(mouseX, mouseY):
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
    seconds = time % 60
    minutes = (time // 60) % 60
    hours = time // 3600
    secPart = ""
    minPart = ""
    hourPart = ""

    # formatting seconds
    if seconds < 10:
        secPart = ":0" + str(seconds)
    else:
        secPart = ":" + str(seconds)

    # formatting minutes
    if hours != 0 and minutes < 10:
        minPart = "0" + str(minutes)
    else:
        minPart = str(minutes)

    # formatting hours
    if hours == 0:
        hourPart = ""
    else:
        hourPart = str(hours) + ":"

    return str(hourPart + minPart + secPart)


def updateWindow(board, playTime):
    WINDOW.fill((255, 255, 255))
    board.draw()
    drawHUD(playTime)
    pygame.display.update()


def main():
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 540, 540)
    startTime = time.time()
    key = None

    running = True
    while running:

        playTime = round(time.time() - startTime)

        # look for any event
        for event in pygame.event.get():
            # close button
            if event.type == pygame.QUIT:
                running = False
            # mouse pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouseX = pos[0]
                mouseY = pos[1]
                board.unselectAll()
                # board click
                if board.clicked(mouseX, mouseY):
                    board.select(mouseX, mouseY)
                # reset button click
                elif checkResetClick(mouseX, mouseY):
                    startTime = time.time()
                    board.reset()
                # solve button click
                elif checkSolveClick(mouseX, mouseY):
                    board.update()
                    board.solveGUI(playTime)
            # mouse pressed
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

        updateWindow(board, playTime)


main()
pygame.quit()
