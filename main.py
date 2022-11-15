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
    app.hudHeight = app.height-app.cols*app.cellSize
    #sliderBox is the coordinates for the bounding box of the attack slider
    app.sliderBox = (app.width*0.35,
                    app.cols*app.cellSize+app.hudHeight/2-app.hudHeight*0.3,
                    app.width*7/8,
                    app.cols*app.cellSize+app.hudHeight/2+app.hudHeight*0.3)
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

def sliderColor(player):
    """when proportion is 0.0, slider is green, when proportion is 1.0,
    the slider is red. The color ranges from green to red depending
    on the proportion selected"""
    r = int(255*player.attackProportion)
    g = int(255*(1-player.attackProportion))
    b = int(100*(1-player.attackProportion))
    return "#"+hex(r)[2:]+hex(g)[2:]+hex(b)[2:]

def drawHud(app,canvas):
    #Hud border with game board
    canvas.create_line(0,app.cellSize*app.cols,app.width,app.cellSize*app.cols,
    fill = "red",width = 3)

    #Displaying player money
    #The id of the player is always 0
    player = app.dict[0]
    font=('Comic Sans MS', 20, 'bold italic')
    x, y = app.width/8, app.cellSize*app.cols+app.hudHeight/2
    canvas.create_text(x, y, text=f'{player.money}', fill='green', font=font)

    #Displaying slider
    x0,y0,x1,y1 = app.sliderBox
    canvas.create_rectangle(x0,y0,x1,y1,outline="black",fill="#303030")
    canvas.create_rectangle(x0,y0,x0+(x1-x0)*player.attackProportion,y1,
    fill=sliderColor(player),outline="black")
    attackMon = int(player.money*player.attackProportion)
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text=f'{attackMon}', 
    fill='white', font=font)


def keyPressed(app, event):
    return

def timerFired(app):
    return

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawHud(app, canvas)

def runGame():
    width, height = dimensions()
    runApp(width=width, height=height)


def main():
    runGame()

main()
