import math, copy, random

from cmu_112_graphics import *
from countryObject import *

#returns width, hight
def dimensions():
    width = 800
    height = 900
    return width,height

def appStarted(app):
    app.width, app.height = dimensions()
    app.cellSize = 10
    app.rows = 80
    app.cols = 80
    app.players = 1
    app.defaultFill = "#1A1A1A"
    app.countryColors = ["blue"] #To be expanded in the future
    #Dictionary that supports using a country's integer id to find the
    #corrsponding country object
    app.dict = {}

    #Initialize the board with -1s. The -1s show the current tile is empty.
    app.board = []
    for i in range(app.rows):
        app.board.append([-1]*app.cols)

    #Add countries in at random positions (1 for now)
    for i in range(app.players):
        row = random.randint(0,app.rows-1)
        col = random.randint(0,app.cols-1)
        #If the tile is already occupied, keep rolling random
        while (app.board[row][col] == 0):
            row = random.randint(0,app.rows-1)
            col = random.randint(0,app.cols-1)
        app.dict[i] = country(i,app.countryColors[i])
        app.board[row][col] = i

def drawBoard(app,canvas):
    #Drawing all cells
    for i in range(app.rows):
        for j in range(app.cols):
            x0, y0 = i*app.cellSize, j*app.cellSize
            x1, y1 = x0+app.cellSize, y0+app.cellSize
            id = app.board[i][j]
            fill = app.defaultFill
            if (id != -1):
                fill = app.dict[id].color
            canvas.create_rectangle(x0,y0,x1,y1,fill=fill,outline=fill)

def drawHud(app,canvas):
    return

def keyPressed(app, event):
    return

def timerFired(app):
    return

def redrawAll(app, canvas):
    drawBoard(app, canvas)

def runGame():
    width, height = dimensions()
    runApp(width=width, height=height)


def main():
    runGame()

main()
